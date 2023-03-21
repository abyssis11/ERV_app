from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from main.models import ERV, Worker
from django.http import HttpResponse
from django.db.models import Q 
import re
from datetime import datetime

# Create your views here.
def homepage(request):
    return render(request, 'base_generic.html')

def category_list(request):
    jobs = Job.objects.all()
    context = {'jobs': jobs}
    return render(request, 'partials/category_selection.html', context=context)

def search_worker(request):
    post = ""
    if request.method == "POST":
        worker = ERV.objects.all()
        value = request.POST
        for key in value:
            post += '  ||||  '+key+"    ////   "+request.POST[key]
            if key == 'search_worker' and  value[key]:
                for term in value[key]:
                    worker = worker.filter( Q(worker__name__icontains = term) | Q(worker__surname__icontains = term))
            if key == 'daterange' and value[key]:
                dates = re.split(' - ', value[key])
                date1 = dates[0]
                date2 = dates[1]
                worker = worker.filter(current_date__range = [datetime.strptime(date1, '%Y-%m-%d').date(), datetime.strptime(date2, '%Y-%m-%d').date()])
            if key == 'category' and value[key]:
                worker = worker.filter(worker__job__category = value[key])
            if key == 'month' and value[key]:
                worker =  worker.filter(current_date__month = value[key])

    results = worker
    context = {'results': results, 'post': post}
    return render(request, 'partials/result_searched_workers_tables.html', context)


def worker_list(request):
    workers= ERV.objects.all()

    context = {'workers': workers}
    return render(request, 'main/worker_list.html', context=context)

def filter(request):
    return render(request, 'partials/filter.html')


