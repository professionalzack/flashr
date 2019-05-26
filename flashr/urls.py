from django.urls import path
from . import views

urlpatterns = [
  path('', views.landing, name='landing'),
  path('question/<int:pk>', views.question_show, name='question_show'),
  path('deck/<slug:tag>', views.deck_create, name='deck_create'),
  path('deck/<slug:tag>/<int:idx>', views.deck_show, name='deck_show'),
  path('pain', views.send_pain, name='send_pain'),
  path('answer', views.answer_me, name='answer_me'),
]
