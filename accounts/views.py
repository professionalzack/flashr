from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProfileForm
from .models import Profile
from flashr.models import Question, Answer

# Create your views here.
def register(request):
  if request.method == 'POST':
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

  # Validation!
    if password == password2:
      if User.objects.filter(username=username).exists():
        return render(request, 'accounts/register.html', {'error': 'That username has already been registered. Please try a different username'})
      else:
        if User.objects.filter(email=email).exists():
          return render(request, 'accounts/register.html', {'error': 'That email has already been registered'})
        else:
          # worked !
          user = User.objects.create_user(username=username, password=password, email=email)
          user.save()
          Profile.objects.create(user_id=user.id)
          return redirect('login')
    else:
      return render(request, 'accounts/register.html', {'error': 'Passwords do not match'})
  else:
    return render(request, 'accounts/register.html')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      return redirect('profile')
    else:
      return render(request, 'accounts/login.html', {'error': 'Invalid Credentials...'})

  else:
    return render(request, 'accounts/login.html')

def logout(request):
  auth.logout(request)
  return redirect('register')#in the future this should be to the landing

@login_required
def profile_create(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('artist_list')
    else:
        form = ProfileForm()
    return render(request, 'accounts/profile_form.html', {'form': form})

@login_required
def profile(request):
  profile = request.user.profile
  quests = Question.objects.filter(answer__author=profile).distinct('id')
  print('quests', quests)
  questions = []
  for quest in quests:
    questions.append({'question':quest, 'answer':quest.answer.all()[0]})

  print(questions)
  return render(request, 'accounts/profile.html', {'profile': profile, 'questions': questions})
