# urls.py
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.MyModelAPIView.as_view()),
]
