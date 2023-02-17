import csv
import datetime
from django.db.models import Q
from django.db import transaction
from django.core.management.base import BaseCommand
from main.models import *

ADMINISTRACIJA = ['SPREMAČICE', 'SIC']
FORMAT_DATE = '%d.%m.%Y.'
FORMAT_TIME = '%H:%M:%S'

with open('/app/ERV/main/management/commands/csv_file.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    names = []
    surnames = []
    jobs = []
    file_date = 0
    times = []
    for row in csv_reader:
        surnames.append(row[0])
        names.append(row[1])
        jobs.append(row[-1])
        file_date = row[3]
        times.append(row[4])
    class Command(BaseCommand):
        @transaction.atomic
        def handle(self, *args, **kwargs):
            # jobs_in_db = Job.objects.all()
            for i in range(len(jobs)):
                if not Job.objects.filter(name__iexact=jobs[i]).exists():
                    if jobs[i].upper() in ADMINISTRACIJA:
                        Job(name = jobs[i], category='administracija').save()
                    else:
                        Job(name = jobs[i], category='nastavnici').save()
                        
            for i in range(len(surnames)):
                if not Worker.objects.filter(name__iexact=names[i]).exists() or not Worker.objects.filter(surname__iexact=surnames[i]).exists(): 
                    Worker(name = names[i], surname = surnames[i], job = Job.objects.get(name__iexact=jobs[i])).save()
                else:
                    worker = Worker.objects.get(Q(name__iexact=names[i]) and Q(surname__iexact=surnames[i]))
                    if not worker.active:
                        worker.active=True
                    worker.save()

            for w in Worker.objects.all():
                if w.active:
                    ERV(worker = w, current_date = datetime.strptime(file_date, FORMAT_DATE)).save()

            for i in range(len(surnames)):
                erv = ERV.objects.get(current_date=datetime.strptime(file_date, FORMAT_DATE), worker = Worker.objects.get(Q(name__iexact=names[i]) and Q(surname__iexact=surnames[i])))
                if not erv.enter_time and datetime.strptime(times[i], FORMAT_TIME) < datetime.strptime('12:00:00', FORMAT_TIME):
                    erv.enter_time = datetime.strptime(times[i], FORMAT_TIME)
                    erv.flag='redovni rad'
                else:
                    if erv.exit_time and not erv.enter_time:
                        erv.enter_time=erv.exit_time
                    erv.exit_time = datetime.strptime(times[i], FORMAT_TIME)
                    erv.flag='redovni rad'
                erv.save()
            
            
