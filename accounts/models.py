from django.db import models

# Create your models here.
class Deck(models.Model):
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='deck')
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='deck')
  order_idx = models.IntegerField()

  def __str__(self):
    return self.order_idx
  
class Question(models.Model):
  author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='question')
  title = models.CharField()
  content = models.TextField()
  tags = models.ManyToManyField(Tag)
  #tags and questions must exist before being combined
    #question = //whatever from the form data
    #question.save()
    #tag = Tag.objects.create(content='HTML', color_code=//color function thing)
    #question.tags.add(tag)
  def __str__(self):
    return self.title