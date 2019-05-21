from django.db import models

# Create your models here.
class Pain(models.Model):
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='pain')
  question = models.ForeignKey(Question, on_delete=models. CASCADE, related_name='pain')
  pain_level = models.IntegerField()
  time_stamp = models.DateField.auto_now_add()

  def __str__(self):
    return self.pain_level

class Answer(models.Model):
  author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answer')
  question = models.ForeignKey(Question, on_delete=models. CASCADE, related_name='answer')
  public = models.BooleanField()
  content = models.TextField()

  def __str__(self):
    return self.content

class Tag(models.Model):
  content = models.TextField()
  color_code = models.CharField(max_length=100)