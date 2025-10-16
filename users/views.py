from http.client import responses

from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserProfile
from django.shortcuts import render,redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializer import UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from django.contrib import messages


# HTML pages render
def login_view(request):
    return render(request, 'users/login.html')

def register_view(request):
    return render(request, 'users/register.html')

# register Endpoint tester
@api_view(['GET'])
@permission_classes([AllowAny])
def test_register_endpoint(request):
    return Response(
        {
            'message': 'register GET endpoint  working'
         }
    )

# login endp tester
@api_view(['GET'])
@permission_classes([AllowAny])
def test_login_endpoint(req):
    return Response(
        {
            'message': 'Login Get endpoint working'
        }
    )


# Register user endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(req):
    serializer = UserProfileSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# user login endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(req):
    #email and password from frontend
    email = req.data.get('email')
    raw_password = req.data.get('password')


    try:
        #check email existence
        user = UserProfile.objects.get(email=email)

        #pass verificacion
        pass_match = check_password(raw_password, user.password)

        if pass_match:
            serializer = UserProfileSerializer(user)

            # JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    'message': 'Login success',
                    'user' : serializer.data,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'error' : 'Invalid Password'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
    except  UserProfile.DoesNotExist:
        # when email doesn't exist
        return Response(
            {
                'error': 'User not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(req):
    user = req.user
    return Response(
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'date_created': user.date_created
        }
    )


#register page rendering and form submission
def register_page(req):
    if req.method == 'POST':
        name = req.POST.get('name')
        email = req.POST.get('email')
        password = req.POST.get('password')

        data = {'name': name, 'email': email, 'password': password}
        api_url = 'http://127.0.0.1:8000/users/register/api/'

        response = requests.post(api_url, json=data)

        if response.status_code==201:
            messages.success(req, 'Registration succesful')
            return redirect('login_page')
        else:
            messages.error(req, 'Registration failed. Try again')

    return render(req, 'users/register.html')


#Login page rendering and form submission
def login_page(req):
    if req.method == 'POST':
        email = req.POST.get('email')
        password = req.POST.get('password')

        data = {'email': email, 'password': password}
        api_url = 'http://127.0.0.1:8000/users/login/api'

        response = requests.post(api_url, json=data)

        if response.status_code == 200:
            token_data = response.json()
            req.session['access_token'] = token_data.get('access')
            req.session['refresh_token'] = token_data.get('refresh')
            messages.success(req, 'Login successful')
            return redirect('dashboard_page')
        else:
            messages.error(req, 'Invalid credentials')

    return render(req, 'users/login.html')


