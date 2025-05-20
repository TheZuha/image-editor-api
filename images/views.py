from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Image
from .forms import ImageUploadForm, TransformForm
from PIL import Image as PILImage, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile

@login_required
def gallery(request):
    images = Image.objects.filter(owner=request.user).order_by('-created_at')
    if request.method == 'POST' and 'upload' in request.POST:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.owner = request.user
            img.save()
            return redirect('gallery')
    else:
        form = ImageUploadForm()
    return render(request, 'gallery.html', {'images': images, 'form': form})

@login_required
def transform_image(request, pk):
    image = get_object_or_404(Image, pk=pk, owner=request.user)
    result_url = None

    if request.method == 'POST':
        form = TransformForm(request.POST)
        if form.is_valid():
            ops = form.cleaned_data
            img = PILImage.open(image.original.path)

            if ops['resize_w'] and ops['resize_h']:
                img = img.resize((ops['resize_w'], ops['resize_h']))
            if ops['crop_w'] and ops['crop_h']:
                x, y = ops['crop_x'] or 0, ops['crop_y'] or 0
                img = img.crop((x, y, x+ops['crop_w'], y+ops['crop_h']))
            if ops['rotate']:
                img = img.rotate(ops['rotate'], expand=True)
            if ops['flip']:
                img = img.transpose(PILImage.FLIP_LEFT_RIGHT)
            if ops['mirror']:
                img = img.transpose(PILImage.FLIP_TOP_BOTTOM)
            if ops['wm_text']:
                draw = ImageDraw.Draw(img)
                font = ImageFont.load_default()
                pos = (ops['wm_x'] or 10, ops['wm_y'] or 10)
                draw.text(pos, ops['wm_text'], fill=(255,255,255), font=font)
            if ops['grayscale']:
                img = img.convert('L')
            if ops['sepia']:
                sep = img.convert('RGB')
                px = sep.load()
                for i in range(sep.width):
                    for j in range(sep.height):
                        r,g,b = px[i,j]
                        tr = int(0.393*r + 0.769*g + 0.189*b)
                        tg = int(0.349*r + 0.686*g + 0.168*b)
                        tb = int(0.272*r + 0.534*g + 0.131*b)
                        px[i,j] = (min(tr,255),min(tg,255),min(tb,255))
                img = sep
            fmt = ops['fmt']
            quality = ops['quality'] or 85
            buf = BytesIO()
            img.save(buf, format=fmt, quality=quality)
            new_name = f"trans_{image.id}.{fmt.lower()}"
            image.original.save(new_name, ContentFile(buf.getvalue()), save=True)
            result_url = image.original.url
    else:
        form = TransformForm(initial={'image_id': image.id})

    return render(request, 'transform.html', {
        'form': form,
        'image': image,
        'result_url': result_url,
    })
