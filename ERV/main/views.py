from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from main.models import ERV

# Create your views here.

class WorkerList(ListView):
    model = ERV

from django.http import HttpResponse
# Create your views here.

def homepage(request):
    return render(request, 'base_generic.html')
