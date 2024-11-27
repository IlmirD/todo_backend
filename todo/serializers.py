from rest_framework import serializers
from django.contrib.auth.models import User

from .models import ToDo

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        email = attrs['email'].lower()
        username = attrs['username'].lower()
        password = attrs['password']
        password2 = attrs['password2']

        check_email = User.objects.filter(email=email).first()
        if check_email:
            raise serializers.ValidationError({'error': 'Этот email недоступен.'})

        check_username = User.objects.filter(username=username).first()
        if check_username:
            raise serializers.ValidationError({'error': 'Это имя пользователя недоступно.'})

        if len(username) <= 4:
            raise serializers.ValidationError({'error': "Минимальная длина имени пользователя 5 символов."})
        
        if len(username) > 25:
            raise serializers.ValidationError({'error': "Максимальная длина имени пользователя 25 символов."})

        if password != password2:
            raise serializers.ValidationError({'error': "Пароли не совпадают."})

        if len(password) <= 7 or len(password2) <= 7:
            raise serializers.ValidationError({'error': "Минимальная длина пароля 8 символов."})

        if len(password) > 25 or len(password2) > 25:
            raise serializers.ValidationError({'error': "Максимальная длина пароля 25 символов."})        
        
        return attrs

    def save(self):
        email = self.validated_data['email'].lower()
        username = self.validated_data['username'].lower()
        password = self.validated_data['password']

        user = User(
            email=email,
            username = username,
        )

        user.set_password(password)
        user.save()

        return User


# для просмотра
class ToDoSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateField(format="%d %b")

    class Meta:
        model = ToDo
        fields = "__all__"

# для создания
class CreateToDoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ToDo
        fields = ["title", "description"]


# для обновления
class UpdateToDoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ToDo
        fields = ["title", "description", "status"]
