from django import forms
from .models import Answer

class Answer(forms.ModelForm):
    
    class Meta:
        model = Answer
        fields = ('content')