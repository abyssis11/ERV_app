from django import forms
from .models import ERV

class ErvForm(forms.ModelForm):
    class Meta:
        model=ERV
        fields = ['worker', 'current_date', 'enter_time', 'exit_time', 'flag', 'processed']