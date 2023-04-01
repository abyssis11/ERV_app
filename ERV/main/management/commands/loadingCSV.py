import csv
import datetime
# from django.db.models import Q
from django.db import transaction
from django.core.management.base import BaseCommand
from main.models import *

ADMINISTRACIJA = ['SPREMAČICE', 'SIC'] # EXPAND
FORMAT_DATE = '%d.%m.%Y.'
FORMAT_TIME = '%H:%M:%S'

def ervExists(worker, date):
    if ERV.objects.filter(current_date= datetime.strptime(date, FORMAT_DATE), worker__id = worker.id).exists():
        return True
    else:
        return False
    
def isProcessed(name, surname, date):
    if Worker.objects.filter(name__iexact = name, surname__iexact = surname).exists():
        worker = Worker.objects.get(name__iexact = name, surname__iexact = surname)
        if ervExists(worker, date):
            erv = ERV.objects.get(current_date = datetime.strptime(date, FORMAT_DATE), worker = worker)
            if erv.processed == True:
                return True
    return False

def timeDifference(date, t1, t2) -> datetime:
    t1 = datetime.combine(datetime.strptime(date, FORMAT_DATE), t1)
    delta = [x for x in str(t2 - t1).split(', ')][1]
    return datetime.strptime(delta, FORMAT_TIME)

with open('/app/ERV/main/management/commands/csv_file.csv') as csv_file:
    # getting delimiter
    testLine = csv_file.readline()
    dialect = csv.Sniffer().sniff(testLine)
    #print(dialect.delimiter)

    # MAYBE ADD ACCEPTED DELIMITERS!

    # return to beginning 
    csv_file.seek(0)
    csv_reader = csv.reader(csv_file, dialect)
    #csv_reader = csv.reader(csv_file, delimiter=',')

    surnames = []
    names = []
    jobs = []
    dates = []
    times = []

    for row in csv_reader:
        surnames.append(row[0])
        names.append(row[1])
        jobs.append(row[-1])
        dates.append(row[3])
        times.append(row[4])

    class Command(BaseCommand):
        @transaction.atomic
        def handle(self, *args, **kwargs):
            for i in range(len(surnames)):
                # skip if row is already processed
                if isProcessed(names[i], surnames[i], dates[i]):
                    continue

                # adding new job to db
                if not Job.objects.filter(name__iexact=jobs[i]).exists():
                    if jobs[i].upper() in ADMINISTRACIJA:
                        Job(name = jobs[i], category='Administracija').save()
                    else:
                        Job(name = jobs[i], category='Nastavnici').save()

                # adding new worker to db
                if not Worker.objects.filter(name__iexact = names[i], surname__iexact = surnames[i]).exists(): 
                    Worker(name = names[i], surname = surnames[i], job = Job.objects.get(name__iexact=jobs[i])).save()
                # if worker is in db, but not active, make it active because it appears in csv file 
                else:
                    worker = Worker.objects.get(name__iexact = names[i], surname__iexact = surnames[i])
                    if not worker.active:
                        worker.active=True
                    worker.save()

                worker = Worker.objects.get(name__iexact = names[i], surname__iexact = surnames[i])
                # checking if ERV already exsists
                if ervExists(worker, dates[i]):
                    # updating ERV

                    # if there are multiple times after 12pm and difference between them is greater then 2 mins 
                    # then the first of them is actually the enter time
                    erv = ERV.objects.get(current_date = datetime.strptime(dates[i], FORMAT_DATE), worker = Worker.objects.get(name__iexact = names[i], surname__iexact = surnames[i]))
                    if erv.exit_time and not erv.enter_time and timeDifference(dates[i], erv.exit_time, datetime.strptime(times[i], FORMAT_TIME)) > datetime.strptime('00:02:00', FORMAT_TIME):
                            erv.enter_time=erv.exit_time
                    erv.exit_time = datetime.strptime(times[i], FORMAT_TIME).time()
                    erv.save()
                else:
                    # if the time is lower then 12pm then that is enter time otherwise that is exit time
                    if datetime.strptime(times[i], FORMAT_TIME) <= datetime.strptime('12:00:00', FORMAT_TIME):
                        ERV(worker = worker, current_date = datetime.strptime(dates[i], FORMAT_DATE), enter_time = datetime.strptime(times[i], FORMAT_TIME).time(), flag = 'Redovni rad').save()
                    else:
                        ERV(worker = worker, current_date = datetime.strptime(dates[i], FORMAT_DATE), exit_time = datetime.strptime(times[i], FORMAT_TIME).time(), flag = 'Redovni rad').save()
            
            # for all the processed ervs (rows), mark them as processed
            for i in range(len(surnames)):
                worker = Worker.objects.get(name__iexact = names[i], surname__iexact = surnames[i])
                erv = ERV.objects.get(current_date = datetime.strptime(dates[i], FORMAT_DATE), worker = worker)
                erv.processed = True
                erv.save()

                

