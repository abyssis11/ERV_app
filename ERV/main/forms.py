from django import forms
from .models import ERV, Worker

class ErvForm(forms.ModelForm):
    class Meta:
        model=ERV
        fields = ['worker', 'current_date', 'enter_time', 'exit_time', 'flag', 'processed']
        widgets = {
            'current_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'enter_time': forms.widgets.TimeInput(attrs={'type': 'time'}),
            'exit_time': forms.widgets.TimeInput(attrs={'type': 'time'})
        }

class WorkerForm(forms.ModelForm):
    class Meta:
        model=Worker
        fields = ['name', 'surname', 'active', 'job']