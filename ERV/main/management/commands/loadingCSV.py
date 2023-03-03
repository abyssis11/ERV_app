import csv
import datetime
from django.db.models import Q
from django.db import transaction
from django.core.management.base import BaseCommand
from main.models import *

ADMINISTRACIJA = ['SPREMAČICE', 'SIC'] # NADOPUNITI
FORMAT_DATE = '%d.%m.%Y.'
FORMAT_TIME = '%H:%M:%S'
# last marker / last visited index in csv file
MARKER = Marker.objects.last()

with open('/app/ERV/main/management/commands/csv_file.csv', 'r+') as csv_file:
    # continuing from last marker
    csv_file.seek(MARKER.value+1)
    csv_reader = csv.reader(csv_file, delimiter=',')

    surnames = []
    names = []
    jobs = []
    row_date = []
    times = []

    for row in csv_reader:
        surnames.append(row[0])
        names.append(row[1])
        jobs.append(row[-1])
        row_date.append(row[3])
        times.append(row[4])

    unique_date = list(set(row_date))

    # if surnames is empty then csv_reader is empty and there is nothing to save/read
    if len(surnames) != 0:
        class Command(BaseCommand):
            @transaction.atomic
            def handle(self, *args, **kwargs):
                for i in range(len(jobs)):
                    # adding new job to db
                    if not Job.objects.filter(name__iexact=jobs[i]).exists():
                        if jobs[i].upper() in ADMINISTRACIJA:
                            Job(name = jobs[i], category='administracija').save()
                        else:
                            Job(name = jobs[i], category='nastavnici').save()
                
                # SPOJI S OVIM GORE
                for i in range(len(surnames)):
                    # adding new worker to db
                    if not Worker.objects.filter(name__iexact=names[i]).exists() or not Worker.objects.filter(surname__iexact=surnames[i]).exists(): 
                        Worker(name = names[i], surname = surnames[i], job = Job.objects.get(name__iexact=jobs[i])).save()
                    # if worker is in db, but not active, we make it active 
                    else:
                        worker = Worker.objects.get(Q(name__iexact=names[i]) and Q(surname__iexact=surnames[i]))
                        if not worker.active:
                            worker.active=True
                        worker.save()

                # for every active worker, the new ERV(record of working hours) for every date is added
                # sta ako dodje samo jedna osoba u subotu? svi dobiju erv
                for w in Worker.objects.all():
                    if w.active:
                        for i in range(len(unique_date)):
                            ERV(worker = w, current_date = datetime.strptime(unique_date[i], FORMAT_DATE)).save()

                # filing ERV data
                for i in range(len(surnames)):
                    erv = ERV.objects.get(current_date=datetime.strptime(row_date[i], FORMAT_DATE), worker = Worker.objects.get(Q(name__iexact=names[i]) and Q(surname__iexact=surnames[i])))
                    # if enter time is null and the time is lower then 12h then that is enter time
                    if not erv.enter_time and datetime.strptime(times[i], FORMAT_TIME) < datetime.strptime('12:00:00', FORMAT_TIME):
                        erv.enter_time = datetime.strptime(times[i], FORMAT_TIME)
                        erv.flag='redovni rad'
                    else:
                        # if first time is after 12h that is actually enter time
                        if erv.exit_time and not erv.enter_time:
                            erv.enter_time=erv.exit_time
                        erv.exit_time = datetime.strptime(times[i], FORMAT_TIME)
                        erv.flag='redovni rad'
                    erv.save()

        # saving new position to marker
        currentMarker = csv_file.tell()
        Marker(value = currentMarker).save()

    else:
        class Command(BaseCommand):
            def handle(self, *args, **options):
                print('Nothing new to add')
                

