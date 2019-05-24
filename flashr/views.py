from django.shortcuts import render, redirect
from django.db.models import Count
from django.http import HttpResponse
from .models import Tag, Question, Deck

#deck_create needs to receive a tag
#deck_create pain level pain_level issue discuss

# Landing
def index(request):
      return HttpResponse("hello, world you are at card question")

def landing(request):
  all_tags = Tag.objects.all().annotate(num_questions=Count('question')).order_by('-num_questions')
  top_tags = all_tags[0:3]
  return render(request, 'flashr/landing.html', {'all_tags': all_tags, 'top_tags': top_tags})

#Questions
def question_show(request, pk):
  question = Question.objects.get(pk=pk)
  return render(request, 'flashr/card.html', {'question': question})

#Deck
##show one deck item
def deck_show(request, tag, idx):
  user = request.user 
  deck = Deck.objects.filter(profile=user.profile) #grabs the subquery so only one db delve
  card = deck.get(order_idx=idx).question #gets the single card in question
  count = deck.count() #counts the cards obv
  return render(request, 'flashr/card_deck.html', {'question': card, 'tag': tag, 'idx': idx, 'count':count})

def deck_create(request, tag): 
  user = request.user 
  Deck.objects.filter(profile=user.profile).delete()
  tag.lower()
  deck = Question.objects.filter(tags__content=tag)
  
  for idx, card in enumerate(deck):
    Deck.objects.create(profile=user.profile, question=deck[idx], order_idx=(idx+1))
  return redirect('deck_show', tag=tag, idx=1)