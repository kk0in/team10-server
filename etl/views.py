from .serializers import *
from rest_framework import generics, permissions, status
from .models import *
from authentication.serializers import UserDetailSerializer
from .permissions import *
from .paginations import *
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseNotAllowed, HttpResponse
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from rest_framework.response import Response


class AnnouncementListView(generics.ListAPIView):
    pagination_class = PostListPagination
    # permission_classes = [IsQualified]
    queryset = Post.objects.filter(is_announcement=True)
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)


class AnnouncementDetailView(generics.RetrieveAPIView):
    permission_classes = [IsQualified | IsAdmin]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class AnnouncementCreateView(generics.CreateAPIView):
    permission_classes = [IsProfessorOrReadOnly]
    serializer_class = AnnouncementCreateSerializer


class AnnouncementUpdateView(generics.UpdateAPIView):
    permission_classes = [IsProfessorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class AnnouncementDeleteView(generics.DestroyAPIView):
    permission_classes = [IsProfessorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class QuestionListView(generics.ListAPIView):
    pagination_class = PostListPagination
    permission_classes = [IsQualified | IsAdmin]
    queryset = Post.objects.filter(is_announcement=False)
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)


class QuestionDetailView(generics.RetrieveAPIView):
    permission_classes = [IsQualified | IsAdmin]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class QuestionCreateView(generics.CreateAPIView):
    permission_classes = [IsQualified | IsAdmin]
    serializer_class = PostCreateSerializer


class QuestionUpdateView(generics.UpdateAPIView):
    permission_classes = [IsQualified | IsAdmin]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class QuestionDeleteView(generics.DestroyAPIView):
    permission_classes = [IsQualified | IsAdmin]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class CommentCreateView(generics.CreateAPIView):
    permission_classes = [IsQualified | IsAdmin]
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        comment = Comment.objects.create(post_id=self.kwargs['pk'], content=request.data['content'], created_by=request.user)
        serializer = CommentSerializer(comment)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ClassListView(generics.ListAPIView):
    permission_classes = [IsQualified]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class ClassCreateView(generics.CreateAPIView):
    permission_classes = [IsProfessorOrReadOnly]
    serializer_class = ClassSerializer


# 수강신청에 사용하는 클래스. 수강신청 후 다시 유저정보를 불러와야 하므로 GET 요청으로 처리함.
class EnrollClassView(generics.RetrieveAPIView):
    # permission_classes = [DoesUserMatchRequest]
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    def get(self, *args, **kwargs):
        # url 형식을 'etl/<int:pk>/enroll/?class_id={클래스 아이디}' 형식으로, class_id를 패러미터로 받기 때문에 이를 parsing
        class_id = int(self.request.GET['class_id'])
        lecture = Class.objects.get(id=class_id)
        # 아래 코드가 이해되지 않는다면 models.py의 Class model 참조 바람.
        self.request.user.classes.add(lecture)
        return super().get(self, *args, **kwargs)


# 수업 드랍에 사용하는 클래스. 드랍 후 다시 유저정보를 불러와야 하므로 GET 요청으로 처리함.
class DropClassView(generics.RetrieveAPIView):
    # permission_classes = [DoesUserMatchRequest]
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    # 코드에 대한 설명은 EnrollClassView 와 유사하므로 이를 참조하기 바람.
    def get(self, *args, **kwargs):
        class_id = int(self.request.GET['class_id'])
        lecture = Class.objects.get(id=class_id)
        self.request.user.classes.remove(lecture)
        return super().get(self, *args, **kwargs)


class StudentListView(generics.ListAPIView):
    pagination_class = StudentListPagination
    serializer_class = UserSimpleSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return User.objects.filter(classes=self.kwargs['pk'])
