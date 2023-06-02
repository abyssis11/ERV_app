from django.shortcuts import render, redirect
from django.views.generic import ListView
from main.models import *
from django.http import HttpResponse
from django.core.files.storage import default_storage
from ERV.settings import BASE_DIR
from utils.loadingCSV_from_upload import uploading_csv, validate_file_extension, validate_file_content_type
from utils.bar_graph_data import graph_data_dict, specific_pie_chart, total_pie_chart
from django.contrib import messages
from main.tables import ProductHTMxMultiColumnTable
from main.filters import ErvFilter
from django.core.paginator import Paginator, EmptyPage
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .forms import  AddErvForm, WorkerForm, EditErvForm
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2.export.views import ExportMixin
import json 

# Create your views here.
class WorkerList(ListView):
    model = ERV

@login_required
def homepage(request):
    return render(request, 'base_generic.html')

@login_required
def upload_form(request):
    return render(request, 'partials/upload_form.html')

@login_required
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

@login_required    
def add_erv(request):
    if request.method == "POST":
        form = AddErvForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ERV uspješno dodan')
            return HttpResponse(status=200, headers={'HX-Trigger': 'Changed'})
    else:
        form = AddErvForm()
    return render(request, 'partials/erv_form.html', {
        'form': form,
    })

@login_required
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

""" class ErvTable(LoginRequiredMixin, SingleTableMixin, FilterView, ExportMixin):
    table_class = ProductHTMxMultiColumnTable
    #queryset = ERV.objects.all()
    model = ERV
    filterset_class = ErvFilter
    paginate_by = 10
    paginator_class = CustomPaginator
    export_formats = ['csv', 'xls']

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
 """


class ErvTable(ExportMixin, SingleTableMixin, FilterView, LoginRequiredMixin):
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

class SwapErvTable(ExportMixin, SingleTableMixin, FilterView, LoginRequiredMixin):
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


class Jobs(LoginRequiredMixin, FilterView):
    filterset_class = ErvFilter
    template_name = "partials/jobs_form.html"

@login_required
def edit_erv(request, pk):
    erv = get_object_or_404(ERV, pk=pk)
    if request.method == "POST":
        form = EditErvForm(request.POST, instance=erv)
        if form.is_valid():
            form.save()
            messages.success(request, 'ERV ažuriran')
            return HttpResponse(status=200, headers={'HX-Trigger': 'Changed'})
    else:
        form = EditErvForm(instance=erv)
    return render(request, 'partials/erv_form.html', {
        'form': form,
        'erv': erv,
    })

@login_required
@ require_POST
def remove_erv(request, pk):
    erv = get_object_or_404(ERV, pk=pk)
    erv.delete()
    messages.warning(request, 'ERV uklonjen')
    return HttpResponse(status=200, headers={'HX-Trigger': 'Changed'})

@login_required
def bar_graph(request, pk, year, month='Ukupno'):
    selectedErv = get_object_or_404(ERV, pk=pk)
    selectedWorker = selectedErv.worker
    workerErvs = get_list_or_404(ERV, worker=selectedWorker)
    graphs=graph_data_dict(workerErvs, year)
    context = {
        'bar_chart':json.dumps(graphs['bar_chart']),
        'pie_chart':json.dumps(graphs['pie_chart']),
        'months':['Ukupno']+graphs['bar_chart']['labels'],
        'years':graphs['years'],
        'pk':pk,
        'current_year':year,
        'current_month':month,
        'worker': workerErvs[0].worker.name + ' ' + workerErvs[0].worker.surname
        }
    #print(context)
    return render(request, 'graphs/graph.html', context)

@login_required
def pie(request, pk, year, month='Ukupno'):
    selectedErv = get_object_or_404(ERV, pk=pk)
    selectedWorker = selectedErv.worker
    workerErvs = get_list_or_404(ERV, worker=selectedWorker)
    pie_chart=specific_pie_chart(workerErvs, year, month)
    context = {
        'pie_chart':json.dumps(pie_chart),
        'months':['Ukupno']+pie_chart['months'],
        'pk':pk,
        'current_year':year,
        'current_month':month,
        }
    #print('hi')
    return render(request, 'graphs/specific_pie_chart.html', context)

@login_required
def total_pie(request, year, month='Ukupno'):
    allErvs = get_list_or_404(ERV)
    print(allErvs)
    pie_chart=total_pie_chart(allErvs, year, month)
    context = {
        'pie_chart':json.dumps(pie_chart),
        'months':['Ukupno']+pie_chart['months'],
        'years': pie_chart['years'],
        'current_year':year,
        'current_month':month,
        }
    #print(context)
    return render(request, 'graphs/total_pie_chart.html', context)

@login_required
def total_pie_partial(request, year, month='Ukupno'):
    allErvs = get_list_or_404(ERV)
    print(allErvs)
    pie_chart=total_pie_chart(allErvs, year, month)
    context = {
        'pie_chart':json.dumps(pie_chart),
        'months':['Ukupno']+pie_chart['months'],
        'years': pie_chart['years'],
        'current_year':year,
        'current_month':month,
        }
    #print(context)
    return render(request, 'graphs/total_pie_partial.html', context)