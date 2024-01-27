from django import forms

from education.models import Question

CHOICES = [
        (1, 1),
        (2, 2)
            ]

# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['correct_answer', 'incorrect_answer1', 'incorrect_answer2']

class QuestionForm(forms.Form):
    question = forms.CharField(label='Вопрос:')
    # answer1 = forms.RadioSelect(choices=FAVORITE_COLORS_CHOICES)
    # answer2 = forms.RadioSelect()
    # answer3 = forms.RadioSelect()
