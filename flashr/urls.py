from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('home/', views.landing, name='landing'),
  path('question/', views.question_show, name='question_show'),
  path('deck/', views.deck_show, name='deck_show')
]

  # path('questions/<int:pk>', views.question_show, name='question_show')
