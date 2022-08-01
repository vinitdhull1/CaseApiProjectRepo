from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from .caseapi import *
from .models import File
from django.conf import settings
import json

class case_api(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
        data_obj = file_serializer.save()  
        files = File.objects.get(id=data_obj.id)
        #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        file_path = r""+str(settings.BASE_DIR)+files.file.url
        #print(file_path)
        output = calling_case(file_path,json.load(files.json_file), request.FILES['file'].name)
        append_srlized_data = {'output': "http://"+request.META.get("REMOTE_ADDR")+":8000/"+output}
        return Response(data=append_srlized_data, status=status.HTTP_201_CREATED) 
    else:
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)