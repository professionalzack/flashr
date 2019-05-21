# from django.db import models

# # Create your models here.
# class Deck(models.Model):
#   profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='deck')
#   question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='deck')
#   order_idx = models.IntegerField()

#   def __str__(self):
#     return self.order_idx
  
# class Question(models.Model):
#   author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='question')
#   title = models.CharField()
#   content = models.TextField()
#   tags = models.ManyToManyField(Tag)
#   #tags and questions must exist before being combined
#     #question = //whatever from the form data
#     #question.save()
#     #tag = Tag.objects.create(content='HTML', color_code=//color function thing)
#     #question.tags.add(tag)
#   def __str__(self):
#     return self.title
    
# class Pain(models.Model):
#   profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='pain')
#   question = models.ForeignKey(Question, on_delete=models. CASCADE, related_name='pain')
#   pain_level = models.IntegerField()
#   time_stamp = models.DateField.auto_now_add()

#   def __str__(self):
#     return self.pain_level

# class Answer(models.Model):
#   author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answer')
#   question = models.ForeignKey(Question, on_delete=models. CASCADE, related_name='answer')
#   public = models.BooleanField()
#   content = models.TextField()

#   def __str__(self):
#     return self.content

# class Tag(models.Model):
#   content = models.TextField()
#   color_code = models.CharField(max_length=100)
