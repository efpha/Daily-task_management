from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from .models import Task
from .serializer import TaskSerializer


#Task creation
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(req):
    serializer =TaskSerializer(data=req.data)
    print("Authenticated user:", req.user)

    if serializer.is_valid():
        serializer.save(user=req.user)

        return  Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Get all tasks for loggen in user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(req):
    tasks = Task.objects.filter(user=req.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

#get single task
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_by_id(req, pk):
    try:
        task = Task.objects.get(pk=pk, user=req.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)


#task update
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(req, pk):
    try:
        task = Task.objects.get(pk=pk, user=req.user)
    except Task.DoesNotExist:
        return Response({
            'error': 'Task not found'
        }, status=status.HTTP_404_NOT_FOUND
        )
    serializer = TaskSerializer(task, data=req.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#delete task
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(req, pk):
    try:
        task = Task.objects.get(pk=pk, user=req.user)
        task.delete()
        return Response(
            {
                'message': 'Task deleted succesfully'
            },
            status=status.HTTP_204_NO_CONTENT
        )
    except Task.DoesNotExist:
        return Response(
            {
                'error': "Task not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

# mark task as completed
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_task_complete(req, pk):
    try:
        task = Task.objects.get(pk=pk, user=req.user)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    task.status = 'completed'
    task.save()

    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)
