import django_tables2 as tables
from .models import ERV
from django_tables2.utils import A 


class ProductHTMxMultiColumnTable(tables.Table):
    job_category = tables.Column(accessor='worker.job.category')
    job = tables.Column(accessor='worker.job')
    month = tables.Column(accessor='current_date__month')
    year = tables.Column(accessor='current_date__year')
    update_button = tables.LinkColumn('main:edit_erv', text="Uredi", verbose_name='Uredi', args=[A('pk')], attrs={
    'a': {'class': 'btn btn-primary btn-floating'}
    })
    class Meta:
        model = ERV
        #show_header = False
        template_name = "tables/table.html"
        fields = ("worker", "current_date", "enter_time", "exit_time", "flag", "update_button")
        exclude = ('id','processed', 'flag', 'job_category', 'job', 'month', 'year')
