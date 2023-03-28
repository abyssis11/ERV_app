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
from django.shortcuts import get_object_or_404
import json
from django.views.decorators.http import require_POST

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
        
def add_erv(request):
    if request.method == "POST":
        form = ErvForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ERV uspješno dodan')
            return HttpResponse(status=200, headers={'HX-Trigger': 'Changed'})
    else:
        form = ErvForm()
    return render(request, 'partials/erv_form.html', {
        'form': form,
    })

def add_worker(request):
    if request.method == "POST":
        form = WorkerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Radnik uspješno dodan')
            #HttpResponse(status=200)
            return redirect('main:add_erv')
    else:
        form = WorkerForm()
    return render(request, 'partials/worker_form.html', {
        'form': form,
    })


class CustomPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                # return the last page
                return self.num_pages
            elif int(number) < 1:
                # return the first page
                return 1
            else:
                raise


class ErvTable(SingleTableMixin, FilterView):
    table_class = ProductHTMxMultiColumnTable
    queryset = ERV.objects.all()
    filterset_class = ErvFilter
    paginate_by = 10
    paginator_class = CustomPaginator

    def get_context_data(self, *args, **kwargs):
        context = super(ErvTable, self).get_context_data(*args,**kwargs)
        context['workers'] = Worker.objects.all()
        return context

    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/table_partial.html"
        else:
            template_name = "tables/table_filter.html"
        return template_name
    
class SwapErvTable(SingleTableMixin, FilterView):
    table_class = ProductHTMxMultiColumnTable
    queryset = ERV.objects.all()
    filterset_class = ErvFilter
    paginate_by = 10
    paginator_class = CustomPaginator
    template_name = "tables/swap.html"

    def get_context_data(self,*args, **kwargs):
        context = super(SwapErvTable, self).get_context_data(*args,**kwargs)
        context['workers'] = Worker.objects.all()
        return context
    
class Jobs(FilterView):
    filterset_class = ErvFilter
    template_name = "partials/jobs_form.html"

def edit_erv(request, pk):
    erv = get_object_or_404(ERV, pk=pk)
    if request.method == "POST":
        form = ErvForm(request.POST, instance=erv)
        if form.is_valid():
            form.save()
            messages.success(request, 'ERV ažuriran')
            return HttpResponse(status=200, headers={'HX-Trigger': 'Changed'})
    else:
        form = ErvForm(instance=erv)
    return render(request, 'partials/erv_form.html', {
        'form': form,
        'erv': erv,
    })

@ require_POST
def remove_erv(request, pk):
    erv = get_object_or_404(ERV, pk=pk)
    erv.delete()
    messages.warning(request, 'ERV uklonjen')
    return HttpResponse(status=200, headers={'HX-Trigger': 'Changed'})