import django_tables2 as tables
from .models import ERV
from django_tables2.utils import A 


class ProductHTMxMultiColumnTable(tables.Table):
    # extra cols
    job_category = tables.Column(accessor='worker.job.category')
    job = tables.Column(accessor='worker.job')
    month = tables.Column(accessor='current_date__month')
    year = tables.Column(accessor='current_date__year')
    update_button = tables.TemplateColumn(template_name='partials/edit_button.html', verbose_name='Uredi')

    # formating
    current_date = tables.DateColumn(format='j. E Y.')
    enter_time = tables.TimeColumn(format='H:i')
    exit_time = tables.TimeColumn(format='H:i')
    class Meta:
        model = ERV
        #show_header = False
        template_name = "tables/table.html"
        fields = ("worker", "current_date", "enter_time", "exit_time", "flag", "update_button")
        exclude = ('id','processed', 'flag', 'job_category', 'job', 'month', 'year')
