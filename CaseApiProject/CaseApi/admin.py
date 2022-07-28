from django.contrib import admin
from .models import File

# Register your models here.
@admin.register(File)
class FileInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'case', 'timestamp']

