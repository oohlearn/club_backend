from django.shortcuts import render
from .serializers import ContactSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status


# Create your views here.

# 意見回饋
@api_view(['POST'])
def create_contact(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
