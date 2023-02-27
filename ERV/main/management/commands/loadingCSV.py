import csv
import datetime
from django.db.models import Q
from django.db import transaction
from django.core.management.base import BaseCommand
from main.models import *

ADMINISTRACIJA = ['SPREMAČICE', 'SIC'] # NADOPUNITI
FORMAT_DATE = '%d.%m.%Y.'
FORMAT_TIME = '%H:%M:%S'
MARKER = Marker.objects.last()

with open('/app/ERV/main/management/commands/csv_file.csv', 'r+') as csv_file:
    csv_file.seek(MARKER.value+1)
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

    # ako je file_date ostao 0 onda znaci da je csv_reader prazan
    if file_date:
        class Command(BaseCommand):
            @transaction.atomic
            def handle(self, *args, **kwargs):
                for i in range(len(jobs)):
                    # ako ne postoji posao u bazi dodajemo ga
                    if not Job.objects.filter(name__iexact=jobs[i]).exists():
                        if jobs[i].upper() in ADMINISTRACIJA:
                            Job(name = jobs[i], category='administracija').save()
                        else:
                            Job(name = jobs[i], category='nastavnici').save()
                            
                for i in range(len(surnames)):
                    # ako ne postoji osoba u bazi dodajemo ju
                    if not Worker.objects.filter(name__iexact=names[i]).exists() or not Worker.objects.filter(surname__iexact=surnames[i]).exists(): 
                        Worker(name = names[i], surname = surnames[i], job = Job.objects.get(name__iexact=jobs[i])).save()
                    # ako je u bazi ali je ne aktivna, stavljamo je u aktivnu
                    else:
                        worker = Worker.objects.get(Q(name__iexact=names[i]) and Q(surname__iexact=surnames[i]))
                        if not worker.active:
                            worker.active=True
                        worker.save()
                # za svakog aktivnog radnika dodajemo ERV za taj dan
                for w in Worker.objects.all():
                    if w.active:
                        ERV(worker = w, current_date = datetime.strptime(file_date, FORMAT_DATE)).save()
                # popunjavamo ERV za svakog radnika
                for i in range(len(surnames)):
                    # uzimamo ERV s današnjim danom i imenom i prezimenom radnika
                    erv = ERV.objects.get(current_date=datetime.strptime(file_date, FORMAT_DATE), worker = Worker.objects.get(Q(name__iexact=names[i]) and Q(surname__iexact=surnames[i])))
                    # ako je enter time null i ako je vrijeme manje od 12h onda je to enter time
                    if not erv.enter_time and datetime.strptime(times[i], FORMAT_TIME) < datetime.strptime('12:00:00', FORMAT_TIME):
                        erv.enter_time = datetime.strptime(times[i], FORMAT_TIME)
                        erv.flag='redovni rad'
                    else:
                        # ako postoji prvo vrijeme nakon 12h onda je to zapravo enter time
                        if erv.exit_time and not erv.enter_time:
                            erv.enter_time=erv.exit_time
                        erv.exit_time = datetime.strptime(times[i], FORMAT_TIME)
                        erv.flag='redovni rad'
                    erv.save()

        currentMarker = csv_file.tell()
        Marker(value = currentMarker).save()

    else:
        class Command(BaseCommand):
            def handle(self, *args, **options):
                print('Nothing to new add')
                

