from django import forms
from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    """Form for creating/editing questions."""
    class Meta:
        model = Question
        fields = ['title', 'body', 'strand']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10',
                'placeholder': 'Enter your question title...'
            }),
            'body': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10 resize-y',
                'rows': 6,
                'placeholder': 'Describe your question in detail...'
            }),
            'strand': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10'
            }),
        }



class AnswerForm(forms.ModelForm):
    """Form for creating answers."""
    class Meta:
        model = Answer
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10 resize-y',
                'rows': 4,
                'placeholder': 'Write your answer...'
            }),
        }


