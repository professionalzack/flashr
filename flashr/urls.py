from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('home/', views.landing, name='landing'),
  path('question/', views.question_show, name='question_show'),
  path('deck/<slug:tag>', views.deck_create, name='deck_create')
  path('deck/<slug:tag>/<int:idx>', views.deck_show, name='deck_show')
]
