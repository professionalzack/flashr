from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count, OuterRef, Subquery, F
from django.http import HttpResponse
from .models import Tag, Question, Deck, Pain

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
@login_required
def question_show(request, pk):
  question = Question.objects.get(pk=pk)
  card_tags = question.tags.all()
  return render(request, 'flashr/card.html', {'question': question, 'card_tags': card_tags})

#Deck
##show one deck item
@login_required
def deck_show(request, tag, idx):
  # # Last question pseudocode
  # if id is last one:
  #   redirect success template, success value
  user = request.user
  deck = Deck.objects.filter(profile=user.profile) #grabs the subquery so only one db delve
  count = deck.count() #counts the cards obv
  card = deck.get(order_idx=idx).question #gets the single card in question
  card_tags = card.tags.all() #gets all the tags the question has

  pains = Pain.objects.all().prefetch_related('profile', 'question') # get once and cache in pains variable

  if pains.filter(profile=user.profile,question__id=card.id).exists():
    pain = pains.filter(profile=user.profile,question__id=card.id).latest('time_stamp').level
  else:
    pain = 0
 
  values = {'question': card, 'card_tags': card_tags, 'tag': tag, 'deck_idx': idx, 'count': count, 'pain': pain}
  return render(request, 'flashr/card.html', values)

@login_required
def deck_create(request, tag):
  user = request.user
  tag.lower()
  # Delete records for any existing deck
  Deck.objects.filter(profile=user.profile).delete()
  # Find all the questions for the new deck
  deck = Question.objects.filter(tags__content=tag)

  # Note: targeting specific user part is not fully tested
  # Create a subquery that gets its id # from the calling query. Gets a users latest pain for a specific question
  # values('level')[:1] extracts just the level, trimmed to the latest one based on the order_by sort
  # Using '.latest()', '[0]', and '.level' don't work since they trigger immediate evaluation in the subquery
  user_pain = Pain.objects.filter(profile=user.profile,question__id=OuterRef('pk')).order_by('-time_stamp').values('level')[:1]
  # Use the subquery to add the users latest pain to all of the questions with the deck tag.
  deck_pain = deck.annotate(user_pain=Subquery(user_pain))#.values('user_pain')
  # Now sort but user pain, descending, with nulls first
  deck_sorted = deck_pain.order_by(F('user_pain').desc(nulls_first=True))

  # for idx, card in enumerate(deck):
  #   Deck.objects.create(profile=user.profile, question=deck[idx], order_idx=(idx+1))
  for idx, card in enumerate(deck_sorted):
    Deck.objects.create(profile=user.profile, question=card, order_idx=(idx+1))
  
  return redirect('deck_show', tag=tag, idx=1)