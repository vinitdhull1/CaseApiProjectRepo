from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

class File(models.Model):
  file = models.FileField(blank=False, null=False)
  json_file = models.FileField(blank=False, null=False, validators=[FileExtensionValidator(allowed_extensions=["json"])])
  timestamp = models.DateTimeField(auto_now_add=True)
