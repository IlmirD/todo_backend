from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from .models import ToDo
from . serializers import ToDoSerializer, CreateToDoSerializer, UpdateToDoSerializer, RegistrationSerializer

# Регистрация
class RegistrationViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        response = {}
        if serializer.is_valid():
            serializer.save()
            response = {"success": 1}
        else:
            response = serializer.errors
        return Response(response)


# с помощью viewsets создаем только один url
class ToDoViewSet(viewsets.ViewSet):
    # только для авторизованных пользователей
    permission_classes = (IsAuthenticated,)

    # проверяем есть ли объект в базе
    def get_object(self, pk):
        try:
            return ToDo.objects.get(pk=pk)
        except ToDo.DoesNotExist:
            raise Http404


    def list(self, request):
        
        # фильрация задач
        filter = request.GET["filter"]

        if filter == 'all':
            qs = ToDo.objects.all()
        elif filter == 'true':
            qs = ToDo.objects.filter(status=True)
        else:
            qs = ToDo.objects.filter(status=False)

        serializer = ToDoSerializer(qs, many=True)

        return Response(serializer.data)


    # все это можно сделать и в serializers как в регистрации, но здесь более наглядно и удобнее
    def create(self, request):

        serializer = CreateToDoSerializer(data=request.data)

        response = {}

        # проверяем наличие ошибок
        if serializer.is_valid():

            title = serializer.validated_data['title']
            description = serializer.validated_data['description']

            ToDo.objects.create(title=title, description=description)

            response = {'success': 1}
        else:
            response = {'error': serializer.errors}

        return Response(response)
   
    
    # берем данные о задаче
    def retrieve(self, request, pk=None):

        todo = self.get_object(pk)

        serializer = ToDoSerializer(todo)

        return Response(serializer.data)


    # обновляем задачу
    def update(self, request, pk=None):

        todo = self.get_object(pk)

        serializer = UpdateToDoSerializer(data=request.data)

        response = {}

        if serializer.is_valid():
            title = serializer.validated_data['title']
            description = serializer.validated_data['description']
            status = serializer.validated_data['status']

            todo.title = title
            todo.description = description
            todo.status = status

            todo.save()

            response = {"success": 1}
        
        else:
            response = {"error": serializer.errors}

        return Response(response)


 
    def destroy(self, request, pk=None):
        todo = self.get_object(pk)

        todo.delete()

        return Response({"success": 1})
