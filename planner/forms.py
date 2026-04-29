from django import forms
from .models import StudyTask

class StudyTaskForm(forms.ModelForm):
    class Meta:
        model = StudyTask
        fields = ['title', 'description', 'subject', 'priority', 'due_date', 'estimated_time']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
