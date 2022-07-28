from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from .caseapi import *

class case_api(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
        file_serializer.save()  
        try:
            output = CaseApi().extracting_data(request.FILES['file'],request.POST.get('case'), request.FILES['file'].name)
            append_srlized_data = {'output': "http://"+request.META.get("REMOTE_ADDR")+":8000/"+output}
            return Response(data=append_srlized_data, status=status.HTTP_201_CREATED)
        except Exception as err:
            print("----->",err)
    else:
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)