from rest_framework import serializers

from etl.serializers import ClassSerializer
from .models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class UserDetailSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True, write_only=True)
    classes = ClassSerializer(many=True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['token'] = instance.auth_token.key
        return rep

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'student_id', 'is_professor', 'is_superuser', 'classes']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'student_id']

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['password'])
        user.username = validated_data['username']
        user.student_id = validated_data['student_id']
        user.save()
        Token.objects.create(user=user)
        return user


class UserIDSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['email']
