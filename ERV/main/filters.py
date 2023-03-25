# products/filters.py
import django_filters
from .models import FLAG_CHOICES, CATEGORY_CHOICES
from django import forms
from django_filters.widgets import RangeWidget
from .models import ERV, Job

MONTH_CHOICES = [
    ('1','Siječanj'),
    ('2', 'Veljača'),
    ('3','Ožujak'),
    ('4', 'Travanj'),
    ('5','Svibanj'),
    ('6','Lipanj'),
    ('7', 'Srpanj'),
    ('8', 'Kolovoz'),
    ('9', 'Rujan'),
    ('10', 'Listopad'),
    ('11', 'Studeni'),
    ('12', 'Prosinac')
]

def year_choices():
    choices = []
    years = ERV.objects.values_list('current_date__year', flat=True).distinct()
    years = set(list(years))
    for y in years:
        y=str(y)
        choices.append((y,) + (y,))
    return choices

def job_queryset(request):
    job_category=request.GET.get('job_category')
    if job_category != None and job_category!='':
        return Job.objects.filter(category=job_category)
    else:
        return Job.objects.all()
    

class ErvFilter(django_filters.FilterSet):
    worker = django_filters.CharFilter(label='', method='worker_filter', widget=forms.TextInput(attrs={'list': 'workers'}))
    current_date = django_filters.DateFromToRangeFilter(label='', widget=RangeWidget(attrs={'type': 'date'}))
    enter_time = django_filters.TimeFilter(label='', widget=forms.TimeInput(attrs={'type': 'time'}), lookup_expr=('gte'))
    exit_time = django_filters.TimeFilter(label='', widget=forms.TimeInput(attrs={'type': 'time'}), lookup_expr=('lte'))
    flag = django_filters.ChoiceFilter(empty_label='Sve vrste rada', label='Vrsta rada', choices=FLAG_CHOICES)

    # costum
    job_category = django_filters.ChoiceFilter(empty_label='Sve kategorije', label='Kategorija posla', choices=CATEGORY_CHOICES, method='category_filter', 
                                               widget=forms.Select(attrs={'hx-get':'jobs','hx-trigger':'change', 'hx-target':'#jobs'}))
    job = django_filters.ModelChoiceFilter(empty_label='Svi poslovi',label='Posao', queryset=job_queryset, method='job_filter')
    month = django_filters.ChoiceFilter(empty_label='Svi mjeseci', label='Mjesec', choices=MONTH_CHOICES, method='month_filter')
    year = django_filters.ChoiceFilter(empty_label='Sve godine', label='Godina', choices=year_choices, method='year_filter')
    class Meta:
        model = ERV
        fields = ["year", "month", "job_category", "job", "flag", "worker", "current_date", "enter_time", "exit_time"]

    def worker_filter(self, queryset, name, value):
        try:
            w_name, w_surname = [x for x in str(value).split(' ')]
        except:
            w_name = value
            w_surname = ''
        name_lookup = name + '__name__icontains'
        surname_lookup = name + '__surname__icontains'
        return queryset.filter(**{name_lookup: w_name}, **{surname_lookup: w_surname})
    
    def category_filter(self, queryset, name, value):
         lookup = 'worker__job__category'
         return queryset.filter(**{lookup: value})
    
    def job_filter(self, queryset, name, value):
        lookup = 'worker__job'
        return queryset.filter(**{lookup: value})
    
    def month_filter(self, queryset, name, value):
        lookup='current_date__month'
        return queryset.filter(**{lookup: value})
    
    def year_filter(self, queryset, name, value):
        lookup='current_date__year'
        return queryset.filter(**{lookup: value})
    