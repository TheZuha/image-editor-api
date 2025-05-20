from django.urls import path
from .api_views import ImageUploadView, ImageListView, ImageDetailView, ImageTransformView
from .views import gallery, transform_image

urlpatterns = [
    path('gallery/', gallery, name='gallery'),
    path('transform/<int:pk>/', transform_image, name='transform'),
    
    path('', ImageUploadView.as_view(), name='upload-image'),
    path('list/', ImageListView.as_view(), name='list-images'),
    path('<int:pk>/', ImageDetailView.as_view(), name='detail-image'),
    path('<int:pk>/transform/', ImageTransformView.as_view(), name='transform-image'),
]