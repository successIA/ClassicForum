import sys
from io import BytesIO

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import ModelForm

from PIL import Image

from forum.attachments.models import Attachment


class AttachmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AttachmentForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = True

    class Meta:
        model = Attachment
        fields = ['image']

    def _get_size(self, im, file):
        size = None
        if file.size >= 0.9 * settings.MAX_IMAGE_UPLOAD_SIZE:
            size = (im.width / 1.3, im.height / 1.3)
        elif file.size >= 0.7 * settings.MAX_IMAGE_UPLOAD_SIZE:
            size = (im.width / 1.1, im.height / 1.1)
        return size

    def _resize_image(self, file, size=None):
        resized_image = file
        im = Image.open(file)   
        size = size if size else self._get_size(im, file)
        if size:
            im.thumbnail(size)
            output_stream = BytesIO()
            im.save(output_stream, im.format)
            resized_image = InMemoryUploadedFile(
                output_stream,
                file.field_name, 
                file.name, 
                file.content_type, 
                sys.getsizeof(output_stream), 
                file.charset,
                content_type_extra=file.content_type_extra
            )
        return resized_image

    def clean_image(self, size=None):
        uploaded_image = self.cleaned_data.get('image') 
        if uploaded_image:
            if uploaded_image.size > settings.MAX_IMAGE_UPLOAD_SIZE:                
                raise forms.ValidationError(
                    'File too large. Size should not exceed 500 KB.'
                ) 
            else:                  
                uploaded_image = self._resize_image(uploaded_image, size=size)
        return uploaded_image
