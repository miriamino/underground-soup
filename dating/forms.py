from django import forms
from .models import Answer

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_self', 'answer_other', 'importance', 'public']
        widgets = { 'answer_self' : forms.RadioSelect,
                    'answer_other' : forms.CheckboxSelectMultiple,
                    'importance' : forms.RadioSelect,
                    'public' : forms.CheckboxInput
        }


