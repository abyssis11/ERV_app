from datetime import datetime 
from django import forms
from .models import ERV, Worker

class AddErvForm(forms.ModelForm):
    class Meta:
        model=ERV
        fields = ['worker', 'current_date', 'enter_time', 'exit_time', 'flag', 'processed']
        widgets = {
            'current_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'enter_time': forms.widgets.TimeInput(attrs={'type': 'time'}),
            'exit_time': forms.widgets.TimeInput(attrs={'type': 'time'})
        }

    def clean(self):
        super(AddErvForm, self).clean()

        worker  = self.cleaned_data.get('worker')
        flag  = self.cleaned_data.get('flag')
        enter_time = self.cleaned_data.get('enter_time')
        exit_time = self.cleaned_data.get('exit_time')
        current_date = self.cleaned_data.get('current_date')
        processed = self.cleaned_data.get('processed')

        if flag == None:
            self._errors['flag'] = self.error_class([
                'Morate ispuniti ovo polje'
            ])

        if processed == False:
            self._errors['processed'] = self.error_class([
                'Morate ispuniti ovo polje'
            ])

        if exit_time == None:
            self._errors['exit_time'] = self.error_class([
                'Morate ispuniti ovo polje'
            ])
        if enter_time == None:
            self._errors['enter_time'] = self.error_class([
                'Morate ispuniti ovo polje'
            ])

        if exit_time != None and enter_time != None:
            exit = datetime.combine(current_date, exit_time)
            enter = datetime.combine(current_date, enter_time)
            if exit.time() <= enter.time():
                self._errors['exit_time'] = self.error_class([
                    'Vrijeme izlaska ne može biti prije vremena ulaska'
                ])

        if ERV.objects.filter(current_date = current_date, worker__id = worker.id).exists():
            self._errors['current_date'] = self.error_class([
                'Ovaj ERV već postoji'
            ])
            self._errors['worker'] = self.error_class([
                'Ovaj ERV već postoji'
            ])

        return self.cleaned_data

class EditErvForm(forms.ModelForm):
    class Meta:
        model=ERV
        fields = ['worker', 'current_date', 'enter_time', 'exit_time', 'flag', 'processed']
        widgets = {
            'current_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'enter_time': forms.widgets.TimeInput(attrs={'type': 'time'}),
            'exit_time': forms.widgets.TimeInput(attrs={'type': 'time'})
        }

    def clean(self):
        super(EditErvForm, self).clean()

        worker  = self.cleaned_data.get('worker')
        flag  = self.cleaned_data.get('flag')
        enter_time = self.cleaned_data.get('enter_time')
        exit_time = self.cleaned_data.get('exit_time')
        current_date = self.cleaned_data.get('current_date')
        processed = self.cleaned_data.get('processed')

        if flag == None:
            self._errors['flag'] = self.error_class([
                'Morate ispuniti ovo polje'
            ])

        if processed == False:
            self._errors['processed'] = self.error_class([
                'Morate ispuniti ovo polje'
            ])

        if exit_time == None:
            self._errors['exit_time'] = self.error_class([
                'Morate ispuniti ovo polje'
            ])
        if enter_time == None:
            self._errors['enter_time'] = self.error_class([
                'Morate ispuniti ovo polje'
            ])

        if exit_time != None and enter_time != None:
            exit = datetime.combine(current_date, exit_time)
            enter = datetime.combine(current_date, enter_time)
            if exit.time() <= enter.time():
                self._errors['exit_time'] = self.error_class([
                    'Vrijeme izlaska ne može biti prije vremena ulaska'
                ])

        return self.cleaned_data

class WorkerForm(forms.ModelForm):
    class Meta:
        model=Worker
        fields = ['name', 'surname', 'active', 'job']

    def clean(self):
        super(WorkerForm, self).clean()

        name  = self.cleaned_data.get('name')
        surname = self.cleaned_data.get('surname')

        if Worker.objects.filter(name__iexact = name, surname__iexact = surname).exists():
            self._errors['name'] = self.error_class([
                'Ovaj radnik već postoji'
            ])
            self._errors['surname'] = self.error_class([
                'Ovaj radnik već postoji'
            ])

        return self.cleaned_data



