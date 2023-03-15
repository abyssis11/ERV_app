from csv import reader
from main.models import *
from datetime import datetime
import os
from django.core.exceptions import ValidationError

def uploading_csv(csv_url):
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

    with open(csv_url) as csv_file:
        csv_reader = reader(csv_file, delimiter=',')

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

        #@transaction.atomic
        for i in range(len(surnames)):
            # skip if row is already processed
            if isProcessed(names[i], surnames[i], dates[i]):
                continue
            # adding new job to db
            if not Job.objects.filter(name__iexact=jobs[i]).exists():
                if jobs[i].upper() in ADMINISTRACIJA:
                    Job(name = jobs[i], category='administracija').save()
                else:
                    Job(name = jobs[i], category='nastavnici').save()
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
                erv.exit_time = datetime.strptime(times[i], FORMAT_TIME)
                erv.save()
            else:
                # if the time is lower then 12pm then that is enter time otherwise that is exit time
                if datetime.strptime(times[i], FORMAT_TIME) <= datetime.strptime('12:00:00', FORMAT_TIME):
                    ERV(worker = worker, current_date = datetime.strptime(dates[i], FORMAT_DATE), enter_time = datetime.strptime(times[i], FORMAT_TIME), flag = 'redovni rad').save()
                else:
                    ERV(worker = worker, current_date = datetime.strptime(dates[i], FORMAT_DATE), exit_time = datetime.strptime(times[i], FORMAT_TIME), flag = 'redovni rad').save()
        
        # for all the processed ervs (rows), mark them as processed
        for i in range(len(surnames)):
            worker = Worker.objects.get(name__iexact = names[i], surname__iexact = surnames[i])
            erv = ERV.objects.get(current_date = datetime.strptime(dates[i], FORMAT_DATE), worker = worker)
            erv.processed = True
            erv.save()

def validate_file_extension(file):
    ext = os.path.splitext(file.name)[1]
    valid_extensions = ['.csv']
    if not ext.lower() in valid_extensions:
        #raise ValidationError(u'Unsupported file extension.')
        return False
    else:
        return True
    
def validate_file_content_type(file):
    content_type = file.content_type
    valid_content_types = ['text/csv']
    if not content_type.lower() in valid_content_types:
        return False
    else:
        return True