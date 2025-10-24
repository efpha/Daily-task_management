from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserProfile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializer import UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# Register endpoint tester
@api_view(['GET'])
@permission_classes([AllowAny])
def test_register_endpoint(request):
    return Response({'message': 'Register GET endpoint working'})


# Login endpoint tester
@api_view(['GET'])
@permission_classes([AllowAny])
def login_test(request):
    return Response({'message': 'Login GET endpoint working'})


# Register user endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User login endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    email = request.data.get('email')
    raw_password = request.data.get('password')

    try:
        user = UserProfile.objects.get(email=email)
        pass_match = check_password(raw_password, user.password)

        if pass_match:
            serializer = UserProfileSerializer(user)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'message': 'Login success',
                    'user': serializer.data,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response({'error': 'Invalid Password'}, status=status.HTTP_401_UNAUTHORIZED)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# Get authenticated user profile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return Response(
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'date_created': user.date_created,
        },
        status=status.HTTP_200_OK
    )
