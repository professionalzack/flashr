from django.db.models import Count, OuterRef, Subquery, F, ExpressionWrapper, IntegerField
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.http import HttpResponse
import simplejson as json
from .models import Tag, Question, Deck, Pain, Answer, Vote

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
  profile = request.user.profile
  deck = Deck.objects.filter(profile=profile) #grabs the subquery so only one db delve
  count = deck.count() #counts the cards obv
  card = deck.get(order_idx=idx).question #gets the single card in question
  card_tags = card.tags.all() #gets all the tags the question has
  
  values = {'question': card, 'card_tags': card_tags, 'tag': tag, 'deck_idx': idx}

  if idx == count:
    values['last_card'] = True
  
  try:
    current_answer = Answer.objects.get(author=profile, question=card)
    values['current_answer'] = current_answer
  except ObjectDoesNotExist:
    pass


  try: #updates values to include most recent pain if applicable
    pain = Pain.objects.filter(profile=profile, question=card).latest('time_stamp')#.order_by('-time_stamp')[0:1].get()
    values['pain'] = pain
  except ObjectDoesNotExist: 
    pass
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

@login_required
def card_community(request, pk):
  user = request.user
  question = Question.objects.get(pk=pk)
  card_tags = question.tags.all()

  # Cache all public answers for current question, and all votes for those answers
  answers = Answer.objects.filter(public=True,question=question).prefetch_related('question')
  votes = Vote.objects.filter(answer__question=question).prefetch_related('answer')
  ## get all the users votes
  user_votes = votes.filter(profile=user.profile)
  ## append them to the relevant answer
  user_votes = votes.filter(profile=user.profile,answer_id=OuterRef('pk')).values('vote')
  answers = answers.annotate(user_vote=Subquery(user_votes))

  ## Count up all the votes and sort by the top Answers
  ## Step 1: Count up the yes' and the no's
  # 1. a) Subqueries: Count up number of votes, filtered by answer and vote type. Saves it to 'yes' or 'no', and returns it.
  count_yes = votes.filter(answer__id=OuterRef('pk'),vote=1).values('vote').annotate(yes=Count('vote')).values('yes')
  count_no = votes.filter(answer__id=OuterRef('pk'),vote=-1).values('vote').annotate(no=Count('vote')).values('no')
  # 1. b) Main outer queries: Runs subquery on all answers for current question, saving returned vote counts to each answer.
  # Note: The only thing Coalesce is doing is replacing any 'none' responses with '0'
  answers = answers.annotate(yes_count=Coalesce(Subquery(count_yes, output_field=IntegerField()), 0))
  answers = answers.annotate(no_count=Coalesce(Subquery(count_no, output_field=IntegerField()), 0))
  # answers[0].yes_count
  # answers[0].no_count
  ## Step 2: Subtract no's from yes' and save as the total. (Coalesce setting 0's instead of Nones makes this work)
  annotated = answers.annotate(total_vote=ExpressionWrapper(F('yes_count') - F('no_count'), output_field=IntegerField()))
  # annotated[0].total_vote
  ## Step 3: Sort by the new total_vote field, highest count first.
  annotated_sorted = annotated.order_by(F('total_vote').desc(nulls_last=True))

  ## Notes on aggregate Sum vs annotate Count:
  # Aggregate works for individual answers, but you can't put .aggregate() inside a subquery. It evaluates right away.
  # sum_votes = Vote.objects.filter(answer__id=1).aggregate(yes=Sum('vote'))
  # So instead we need to count up all the Yes votes and all the No votes, and then subtract them

  values = {'question': question, 'card_tags': card_tags, 'answers': annotated_sorted}
  return render(request, 'flashr/card_community.html', values)

## API Endpoints
# Send PAIN API Endpoint
def send_pain(request):
  # print(request.POST)
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
    return HttpResponse(json.dumps({"error": "wasn't a POST request"}), content_type="application/json")

# Send Answer API Endpoint
def send_answer(request):
  print(request.POST)
  if request.method == 'POST':

    profile = request.user.profile

    content = request.POST['content']
    public = ((True, False) [int(request.POST['public']) == 2 ])
    question = Question.objects.get(id=request.POST['question_id'])

    try:
      Answer.objects.get(author=profile,question=question ).delete()
    except ObjectDoesNotExist:
      pass
    
    Answer.objects.create(content=content, public=public, question=question, author=profile)

    response = {}
    response['status'] = 200
    response['content'] = content
    response['public'] = public

    return HttpResponse(json.dumps(response), content_type="application/json")
  else:
    return HttpResponse(json.dumps({"no info": "wasn't a POST request"}), content_type="application/json")

# Send Vote API Endpoint
def send_vote(request):
  # print(request.POST)
  if request.method == 'POST':
    profile = request.user.profile
    vote_choice = int(request.POST['vote'])
    answer = Answer.objects.get(id=request.POST['answer_id'])
    action = request.POST['action']

    # print('vote:', vote_choice)
    # print('type? ', type(vote_choice))
    # print('answer :', answer)
    response = {}
    # Validate the vote value for the expected values
    if (vote_choice == 1) or (vote_choice == -1):
      # print('yes or no vote detected...')
      # Delete any existing votes from this user for this answer
      Vote.objects.filter(profile=profile, answer=answer).delete()
      # Add the user's vote for this question
      Vote.objects.create(vote=vote_choice, answer=answer, profile=profile)
      response['status'] = 200
      response['vote'] = vote_choice
      response['a_id'] = answer.id
    elif (vote_choice == 0):
      # print('un-vote detected...')
      # 0 means they are 'un-voting', ie taking back a vote
      # Delete any existing votes from this user for this answer
      Vote.objects.filter(profile=profile, answer=answer).delete()
      response['status'] = 200
      response['vote'] = vote_choice
      response['action'] = action
      response['a_id'] = answer.id
    else:
      # print('invalid vote detected...')
      # Not a valid vote
      response['status'] = 400
      response['error'] = "Invalid vote option"
    
    return HttpResponse(json.dumps(response), content_type="application/json")
  else:
    return HttpResponse(json.dumps({"error": "wasn't a POST request"}), content_type="application/json")