from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist 
from django.shortcuts import render, redirect
from django.http import HttpResponse
import simplejson as json
from django.db.models import Count
from .models import Tag, Question, Deck, Pain, Answer


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
  card_tags = question.tags.all()
  return render(request, 'flashr/card.html', {'question': question, 'card_tags': card_tags})

#Deck
##show one deck item
def deck_show(request, tag, idx):
  user = request.user
  deck = Deck.objects.filter(profile=user.profile) #grabs the subquery so only one db delve
  count = deck.count() #counts the cards obv
  card = deck.get(order_idx=idx).question #gets the single card in question
  card_tags = card.tags.all() #gets all the tags the question has
  if idx == count:
    idx = 'last'
  values = {'question': card, 'card_tags': card_tags, 'tag': tag, 'deck_idx': idx}
  try: #updates values to include most recent pain if applicable
    pain = Pain.objects.filter(profile=user.profile, question=card).order_by('-time_stamp')[0:1].get()
    values['pain'] = pain
  except ObjectDoesNotExist: #creates a throwaway variable if no pain was found
    pain = 'pain'
  return render(request, 'flashr/card.html', values)

def deck_create(request, tag):
  user = request.user 
  Deck.objects.filter(profile=user.profile).delete()
  tag.lower()
  deck = Question.objects.filter(tags__content=tag)
  # To Do: Sort Deck by User Pain here
  for idx, card in enumerate(deck):
    Deck.objects.create(profile=user.profile, question=deck[idx], order_idx=(idx+1))
  return redirect('deck_show', tag=tag, idx=1)

#PAIN
def send_pain(request):
  print(request.POST)
  if request.method == 'POST':
    profile = request.user.profile
    pain_level = request.POST['level']
    question = Question.objects.get(id=request.POST['question_id'])
    Pain.objects.create(level=pain_level, question=question, profile=profile)

    response = {}
    response['status'] = 200
    response['pain_level'] = pain_level

    return HttpResponse(json.dumps(response), content_type="application/json")
  else:
    return HttpResponse(json.dumps({"erryr": "wasnt a post"}), content_type="application/json")

def answer_me(request):
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
    return HttpResponse(json.dumps({"no info": "wasnt a post"}), content_type="application/json")
