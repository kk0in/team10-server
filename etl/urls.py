from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from . import views


urlpatterns = [
    path('class/', ClassListView.as_view()),
    path('class/enroll/', EnrollClassView.as_view()),
    path('class/drop/', DropClassView.as_view()),
    path('class/<int:pk>/user-list/', StudentListView.as_view()),

    # 공지사항 게시판
    path('announcement/', AnnouncementListView.as_view(), name='announcement_list'),
    path('announcement/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement_detail'),
    path('announcement/comment/create/<int:pk>/', CommentCreateView.as_view(), name='announcement_comment_create'),
    path('announcement/create/', AnnouncementCreateView.as_view(), name='announcement_create'),
    path('announcement/modify/<int:pk>/', AnnouncementUpdateView.as_view(), name='announcement_update'),
    path('announcement/delete/<int:pk>/', AnnouncementDeleteView.as_view(), name='announcement_delete'),

    # 질의응답 게시판
    path('question/', QuestionListView.as_view(), name='question_list'),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('question/comment/create/<int:pk>/', QuestionCreateView.as_view(), name='question_comment_create'),
    path('question/create/', QuestionCreateView.as_view(), name='question_create'),
    path('question/modify/<int:pk>/', QuestionUpdateView.as_view(), name='question_update'),
    path('question/delete/<int:pk>/', QuestionDeleteView.as_view(), name='question_delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
