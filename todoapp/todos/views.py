from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsOwner
from rest_framework.authentication import TokenAuthentication

from todos.models import Todo
from todos.serializers import TodoCreateSerializer


class TodoAPIViewSet(ModelViewSet):
    """
        success response for create/update/get
        {
          "name": "",
          "done": true/false,
          "date_created": ""
        }

        success response for list
        [
          {
            "name": "",
            "done": true/false,
            "date_created": ""
          }
        ]
    """

    queryset = Todo.objects.all()
    serializer_class = TodoCreateSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            todo = self.get_object()
        except Todo.DoesNotExist:
            raise NotFound(
                "Todo not found or you don't have permission to update this Todo.")

        serializer = self.get_serializer(todo, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            todo = self.get_object()
        except Todo.DoesNotExist:
            raise NotFound(
                "Todo not found or you don't have permission to delete this Todo.")

        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
