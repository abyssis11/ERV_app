from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from main.models import ERV, Worker
from django.http import HttpResponse
from django.db.models import Q 
import logging

# Create your views here.
def homepage(request):
    return render(request, 'base_generic.html')


def search_worker(request):
    searched_word = request.POST.get('search_worker')
    
    selected_month = request.GET.get('month')
    ERVs = ERV.objects.all()

    if searched_word != "":
        for term in searched_word.split():
            worker = ERVs.filter( Q(worker__name__icontains = term) | Q(worker__surname__icontains = term))
    else:
        worker = ""
    
    if selected_month != "":
        worker = ERVs.filter(current_date__month = selected_month)


    # if request.POST.get('month'):
    #     worker = worker.filter(current_dat__month = selected_month)

    results = worker

    context = {'results': results}
    return render(request, 'partials/result_searched_workers_tables.html', context)


def worker_list(request):
    workers= ERV.objects.all()

    context = {'workers': workers}
    return render(request, 'main/worker_list.html', context=context)


