from django.contrib import admin
from .models import Tag, Question, Pain, Answer

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Pain)