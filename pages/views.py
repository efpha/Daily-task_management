from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """Return a lightweight status response for the API root."""
    return Response({'message': 'Daily Task Management API is running'})
