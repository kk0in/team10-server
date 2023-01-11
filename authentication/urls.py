from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from . import views

urlpatterns = [
    path('signup/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('set/<int:pk>/', SetUserInfoAPI.as_view()),
    path('idcheck/', IdCheckAPI.as_view()),
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
]

urlpatterns = format_suffix_patterns(urlpatterns)