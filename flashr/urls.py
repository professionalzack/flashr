from django.urls import path
from . import views

urlpatterns = [
  path('home/', views.landing, name='landing'),
  path('questions/<int:pk>', views.question_show, name='question_show')
]