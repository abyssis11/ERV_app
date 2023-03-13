from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from main.models import ERV

# Create your views here.

class IndexView(TemplateView):
    template_name = 'base_generic.html'

class WorkerList(ListView):
    model = ERV

