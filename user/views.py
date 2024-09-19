from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework import viewsets, status
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token


from django.contrib.auth.models import User

from .models import UserProfile
from .serializers import ContactSerializer, CustomerSerializer

from rest_framework.permissions import IsAuthenticated



# 意見回饋
@api_view(['POST'])
def create_contact(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def register_admin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            name = data.get('name')
            work_title = data.get("work_title")

            if not username or not password:
                return JsonResponse({'error': '用戶名和密碼是必須的'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': '用戶名已存在/Email已被使用'}, status=400)

            user = User.objects.create_user(username=username, password=password,
                                            email=email, first_name=name, last_name=work_title)
            UserProfile.objects.create(user=user, user_type='user')

            return JsonResponse({'message': '用戶註冊成功'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': '無效的 JSON 數據'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': '只允許 POST 請求'}, status=405)


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            name = data.get('name')

            if not username or not password:
                return JsonResponse({'error': '用戶名和密碼是必須的'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': '用戶名已存在/Email已被使用'}, status=400)

            user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
            UserProfile.objects.create(user=user, user_type='user')

            return JsonResponse({'message': '用戶註冊成功'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': '無效的 JSON 數據'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': '只允許 POST 請求'}, status=405)


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({"error": "無此帳號"}, status=400)

            user = authenticate(username=user.username, password=password)

            if user is not None:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)

                return JsonResponse({
                    "token": token.key,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "name": user.first_name,
                        "is_staff": user.is_staff,
                        "is_active": user.is_active,
                    },
                    "message": "登入成功"
                }, status=200)
            else:
                return JsonResponse({'error': '帳號或密碼錯誤'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': '無效的 JSON 數據'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': '只允許 POST 請求'}, status=405)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def validate_token(request):
    return Response({'user': {
        'id': request.user.id,
        'email': request.user.email,
        "name": request.user.first_name,
        "is_staff": request.user.is_staff,
        "is_active": request.user.is_active,
    }})
