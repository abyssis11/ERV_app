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
    searched_word = ""
    selected_month = ""
    selected_category = ""
    selected_date = ""
    k=""
    if request.method == "POST":
        if request.POST.get('search_worker'):
            searched_word = request.POST.get('search_worker')
        if request.POST.get('month'):
            selected_month = request.POST.get('month')
        if request.POST.get('category'):
            selected_category = request.POST.get('category')
        if request.POST.get('daterange'):
            selected_date = request.POST.get('daterange')
        
        ERVs = ERV.objects.all()

        if request.POST.get('search_worker') and request.POST.get('month') and request.POST.get('category'):
            for term in searched_word.split():
                worker = ERVs.filter( Q(worker__name__icontains = term) | Q(worker__surname__icontains = term))
            worker = worker.filter(current_date__month = selected_month)
            worker = worker.filter(worker__job__category = selected_category)
        else:
            if request.POST.get('search_worker') and request.POST.get('month'): 
                for term in searched_word.split():
                    worker = ERVs.filter( Q(worker__name__icontains = term) | Q(worker__surname__icontains = term))
                worker = worker.filter(current_date__month = selected_month)
          
            elif request.POST.get('search_worker') and request.POST.get('category'):
                for term in searched_word.split():
                    worker = ERVs.filter( Q(worker__name__icontains = term) | Q(worker__surname__icontains = term))
                worker = ERVs.filter(worker__job__category = selected_category)

            elif request.POST.get('month') and request.POST.get('category'):
                worker = ERVs.filter(current_date__month = selected_month)
                worker = worker.filter(worker__job__category = selected_category)
            
            else:

                if request.POST.get('search_worker'):
                    for term in searched_word.split():
                        worker = ERVs.filter( Q(worker__name__icontains = term) | Q(worker__surname__icontains = term))
                
                if request.POST.get('month'):
                    worker = ERVs.filter(current_date__month = selected_month)
                
                if request.POST.get('category'):
                    worker = ERVs.filter(worker__job__category = selected_category)
                
                if request.POST.get('daterange'):
                    dates = re.split(' - ', selected_date)
                    date1 = dates[0]
                    date2 = dates[1]
                    worker = ERVs.filter(current_date__range = [datetime.strptime(date1, '%Y-%m-%d').date(), datetime.strptime(date2, '%Y-%m-%d').date()])

        if not request.POST.get('search_worker') and not request.POST.get('month') and not request.POST.get('category'):
            worker = ""
    else: 
        results = ""
    results = worker
    # post = request.POST
    context = {'results': results}
    return render(request, 'partials/result_searched_workers_tables.html', context)


def worker_list(request):
    workers= ERV.objects.all()

    context = {'workers': workers}
    return render(request, 'main/worker_list.html', context=context)

def filter(request):
    return render(request, 'partials/filter.html')


