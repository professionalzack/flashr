from django.shortcuts import render
from django.db.models import Count
from .models import Tag, Question
#deck_create needs to recieve a tag
#deck_create pain level pain_level issue discuss
#deck functions w i p, commented out

# Create your views here:
# Landing
def landing(request):
  all_tags = Tag.objects.all().annotate(num_questions=Count('question')).order_by('-num_questions')
  top_tags = all_tags[0:3]
  return render(request, 'flashr/landing.html', {'all_tags': all_tags, 'top_tags': top_tags})

#Questions
def question_show(request, pk):
  question = Question.objects.get(pk=pk)
  return render(request, 'flashr/card.html', {'question': question})

#Deck
def deck_show(request, pk):
  deck = Deck.objects.filter(profile = user.profile)
  return render(request, 'flashr/card_deck.html', {'deck': deck})

def deck_create(request, tag): #is this correct?
  Deck.objects.filter(profile = user.profile).delete()

  deck = Question.objects.filter(tags__content=tag) # tags__ or tags. ?
  # user_pain = Pain.objects.filter(profile = user.profile)

  # pain_list = //FIND MATCHES ON Question BETWEEN user_pain AND tagged_cards
  # SELECT * FROM (SELECT question FROM pain_omdel WHERE profile = user.profile) WHERE tags__content=tag 

  # //ORDER pain_list BY pain_level
  # no_pain = //ALL tagged_cards NOT IN pain_list
  # //deck = no_pain + pain_list

  for idx, card in enumerate(deck):
    Deck.objects.create(profile=user.profile, question=deck[idx], order_idx=(idx+1))
  return redirect('deck_show')