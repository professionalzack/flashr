from django.db.models import Count, OuterRef, Subquery, F
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponse
import simplejson as json
from .models import Tag, Question, Deck, Pain, Answer

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
  user = request.user
  deck = Deck.objects.filter(profile=user.profile) #grabs the subquery so only one db delve
  count = deck.count() #counts the cards obv
  card = deck.get(order_idx=idx).question #gets the single card in question
  card_tags = card.tags.all() #gets all the tags the question has

  current_answer = Answer.objects.get(id=2)
 ##answers w i p // remove current_answer from values and insert dynamically 
  values = {'question': card, 'card_tags': card_tags, 'tag': tag, 'deck_idx': idx, 'current_answer': current_answer}
  if idx == count:
        values['last_card'] = True
  try: #updates values to include most recent pain if applicable
    pain = Pain.objects.filter(profile=user.profile, question=card).latest('time_stamp')#.order_by('-time_stamp')[0:1].get()
    values['pain'] = pain
  except ObjectDoesNotExist: #creates a throwaway variable if no pain was found
    pain = 'pain'
## Alternative method to show pain
#  pains = Pain.objects.all().prefetch_related('profile', 'question') # get once and cache in pains variable
#  if pains.filter(profile=user.profile,question__id=card.id).exists():
#    pain = pains.filter(profile=user.profile,question__id=card.id).latest('time_stamp').level
#  else:
#    pain = None
#  values = {'question': card, 'card_tags': card_tags, 'tag': tag, 'deck_idx': idx, 'count': count, 'pain': pain}
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
  pains = Pain.objects.all().prefetch_related('profile', 'question') # get once and cache in pains variable
  user_pain = pains.filter(profile=user.profile,question__id=OuterRef('pk')).order_by('-time_stamp').values('level')[:1]
  # Use the subquery to add the users latest pain to all of the questions with the deck tag.
  deck_pain = deck.annotate(user_pain=Subquery(user_pain))#.values('user_pain')
  # Now sort but user pain, descending, with nulls first
  deck_sorted = deck_pain.order_by(F('user_pain').desc(nulls_first=True))

  # for idx, card in enumerate(deck):
  #   Deck.objects.create(profile=user.profile, question=deck[idx], order_idx=(idx+1))
  for idx, card in enumerate(deck_sorted):
    Deck.objects.create(profile=user.profile, question=card, order_idx=(idx+1))
  
  return redirect('deck_show', tag=tag, idx=1)

#Send PAIN API Endpoint
def send_pain(request):
  # print(request.POST)
  if request.method == 'POST':
    profile = request.user.profile
    pain_level = request.POST['level']
    question = Question.objects.get(id=request.POST['question_id'])
    Pain.objects.create(level=pain_level, question=question, profile=profile)

    # response = {
    #  'status': 200,
    #  'pain_level: pain_level
    # }
    response = {}
    response['status'] = 200
    response['pain_level'] = pain_level

    return HttpResponse(json.dumps(response), content_type="application/json")
  else:
    return HttpResponse(json.dumps({"error": "wasnt a POST request"}), content_type="application/json")

# Send Answer API Endpoint
def send_answer(request):
  print(request.POST)
  if request.method == 'POST':
    profile = request.user.profile
    content = request.POST['content']
    public = ((True, False) [int(request.POST['public']) == 2 ])
    question = Question.objects.get(id=request.POST['question_id'])
    Answer.objects.create(content=content, public=public, question=question, author=profile)

    response = {}
    response['status'] = 200
    response['content'] = content
    response['public'] = public

    return HttpResponse(json.dumps(response), content_type="application/json")
  else:
    return HttpResponse(json.dumps({"no info": "wasnt a POST request"}), content_type="application/json")
