from django.urls import path

from . import views

urlpatterns = [
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  # path('profile/', views.profile, name='profile'), Do we need this?
  path('profile/', views.profile, name='profile'),
  path('profile/new', views.profile_create, name='profile_create')
]