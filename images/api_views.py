from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from .models import Image
from .serializers import ImageSerializer
from PIL import Image as PILImage, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile

class ImageUploadView(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ImageListView(generics.ListAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user).order_by('-created_at')

class ImageDetailView(generics.RetrieveAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Image.objects.all()

class ImageTransformView(generics.GenericAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        image = get_object_or_404(Image, pk=pk, owner=request.user)
        ops = request.data.get('transformations', {})
        img = PILImage.open(image.original)

        if 'resize' in ops:
            w, h = ops['resize']['width'], ops['resize']['height']
            img = img.resize((w, h))
        if 'crop' in ops:
            x, y = ops['crop']['x'], ops['crop']['y']
            w, h = ops['crop']['width'], ops['crop']['height']
            img = img.crop((x, y, x + w, y + h))
        if 'rotate' in ops:
            img = img.rotate(ops['rotate'], expand=True)
        if ops.get('flip', False):
            img = img.transpose(PILImage.FLIP_LEFT_RIGHT)
        if ops.get('mirror', False):
            img = img.transpose(PILImage.FLIP_TOP_BOTTOM)
        if 'watermark' in ops:
            text = ops['watermark'].get('text', '')
            pos = ops['watermark'].get('position', (10, 10))
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            draw.text(tuple(pos), text, fill=(255,255,255), font=font)
        if ops.get('filters', {}).get('grayscale'):
            img = img.convert('L')
        if ops.get('filters', {}).get('sepia'):
            sepia = img.convert('RGB')
            pixels = sepia.load()
            for i in range(sepia.width):
                for j in range(sepia.height):
                    r, g, b = pixels[i, j]
                    tr = int(0.393*r + 0.769*g + 0.189*b)
                    tg = int(0.349*r + 0.686*g + 0.168*b)
                    tb = int(0.272*r + 0.534*g + 0.131*b)
                    pixels[i, j] = (min(tr,255), min(tg,255), min(tb,255))
            img = sepia
        fmt = ops.get('format', 'JPEG')
        quality = ops.get('compress', {}).get('quality', 85)
        buffer = BytesIO()
        img.save(buffer, format=fmt, quality=quality)
        new_file = ContentFile(buffer.getvalue(), name=f"trans_{image.id}.{fmt.lower()}")
        image.original.save(new_file.name, new_file)
        return Response(ImageSerializer(image).data, status=status.HTTP_200_OK)
