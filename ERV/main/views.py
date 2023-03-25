from django.shortcuts import render, redirect, redirect
from django.views.generic import ListView, TemplateView
from main.models import *
from django.http import HttpResponse
from django.core.files.storage import default_storage
from ERV.settings import BASE_DIR
from utils.loadingCSV_from_upload import uploading_csv, validate_file_extension, validate_file_content_type
from django.contrib import messages
from main.tables import ProductHTMxMultiColumnTable #ProductHTMxTable
from main.filters import ErvFilter
from django.core.paginator import Paginator, EmptyPage
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .forms import  ErvForm, WorkerForm

# Create your views here.
class WorkerList(ListView):
    model = ERV

def homepage(request):
    return render(request, 'base_generic.html')

def upload_form(request):
    return render(request, 'partials/upload_form.html')

def upload_csv(request):
    if request.method == 'POST':
        csv = request.FILES.get('csv')
        if len(request.FILES) != 0 and validate_file_extension(csv) and validate_file_content_type(csv):
            csv_name = default_storage.save('csv_file', csv)
            csv_url = str(BASE_DIR) + default_storage.url(csv_name)
            
            try:
                uploading_csv(csv_url)
                default_storage.delete(csv_url)
                messages.success(request, 'CSV datoteka uspješno učitana')
                return HttpResponse(status=200, headers={'HX-Trigger': 'Changed'})
            except:
                default_storage.delete(csv_url)
                messages.error(request, 'Problem s CSV datotekom')
                return HttpResponse(status=400)
            
        else:
            messages.error(request, 'Potrebno je odabrati CSV datoteku')
            return HttpResponse(status=400)
     