from django import forms
from .models import Image

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['original']
        widgets = {
            'original': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

class TransformForm(forms.Form):
    image_id    = forms.IntegerField(widget=forms.HiddenInput())
    resize_w    = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Width'}))
    resize_h    = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Height'}))
    crop_x      = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Crop X'}))
    crop_y      = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Crop Y'}))
    crop_w      = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Crop Width'}))
    crop_h      = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Crop Height'}))
    rotate      = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Rotate°'}))
    grayscale   = forms.BooleanField(required=False)
    sepia       = forms.BooleanField(required=False)
    quality     = forms.IntegerField(required=False, min_value=1, max_value=100,
                                     widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Quality'}))
    format      = forms.ChoiceField(choices=[('JPEG','JPEG'),('PNG','PNG')], initial='JPEG',
                                     widget=forms.Select(attrs={'class':'form-select'}))
