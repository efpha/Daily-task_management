from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserProfile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializer import UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken

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
def login_test(req):
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

#user's profile
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(req):
    req.session.flush()
    return Response({"message": "Logged out successfully"}, status=200)
