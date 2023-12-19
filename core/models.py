from django.db import models
from django.core.validators import FileExtensionValidator



class Encoding(models.Model):
    file = models.FileField(upload_to='videos/', null = True, verbose_name="", validators=[FileExtensionValidator(allowed_extensions=["MP4"])])
    secret_key = models.CharField(max_length = 80, null = True, blank = True)
    frame_number = models.IntegerField(null = True, blank = True)
    message = models.CharField(max_length = 80, null = True, blank = True)
    encoded_file = models.FileField(upload_to='encoded/', null = True )


class Decoding(models.Model):
    file = models.FileField(upload_to='videos/', null = True, verbose_name="", validators=[FileExtensionValidator(allowed_extensions=["MP4"])])
    secret_key = models.CharField(max_length = 80, null = True, blank = True)
    frame_number = models.IntegerField(null = True, blank = True)
  