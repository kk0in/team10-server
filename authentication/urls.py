from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('signup/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('set/<int:pk>/', SetUserInfoAPI.as_view()),
    path('idcheck/', IdCheckAPI.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)