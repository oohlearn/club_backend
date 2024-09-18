from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework import viewsets, status
from django.http import JsonResponse
import json

from django.contrib.auth.models import User

from .models import UserProfile
from .serializers import ContactSerializer, CustomerSerialize


# 意見回饋
@api_view(['POST'])
def create_contact(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            nickname = data.get('nickname')

            if not username or not password:
                return JsonResponse({'error': '用戶名和密碼是必須的'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': '用戶名已存在/Email已被使用'}, status=400)

            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user, user_type='user')

            return JsonResponse({'message': '用戶註冊成功'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': '無效的 JSON 數據'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': '只允許 POST 請求'}, status=405)
