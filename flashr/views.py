from django.shortcuts import render
#deck_create needs to recieve a tag
#deck_create pain level pain_level issue discuss
#deck functions w i p, commented out


# Create your views here.
#Questions
def question_show(request, pk):
  question = Question.objects.get(pk=pk)
  return render(request, 'flashr/card.html', {'question': question})

#Deck
# def deck_show(request, pk):
#   deck = Deck.objects.filter(profile = user.profile)
#   return render(request, 'flashr/card_deck.html', {'deck': deck})

# def deck_create(request, tag): #is this correct?
#   Deck.objects.filter(profile = user.profile).delete()

#   deck = Question.objects.filter(tags__content=tag)
#     .filter(//NOT SURE DUDE)
#     .extends(Question.objects.filter(tags__content=tag)
#     .order_by(pain.level))

#   for idx, card in enumerate(deck):
#     Deck.objects.create(profile=user.profile, question=deck[idx], order_idx=(idx+1))
#   return redirect('deck_show')