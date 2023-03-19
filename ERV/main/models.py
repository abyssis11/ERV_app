from django.db import models
from datetime import date, datetime 

CATEGORY_CHOICES = {
    ('administracija', 'administracija'),
    ('nastavnici', 'nastavnici')
}

FLAG_CHOICES = {
    ('RR', 'redovni rad'),
    ('PN', 'putni nalog'),
    ('BO', 'bolovanje'),
    ('SL', 'slobodan dan'),
    ('GO', 'godišnji odmor'),
    ('RK', 'rad od kuće')
}


class Job(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
   
    def __str__(self):
        return self.name

class Worker(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name + ' ' + self.surname


class ERV(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name='Radnik')
    current_date = models.DateField('Datum', default=date.today)
    enter_time = models.TimeField('Vrijeme ulaska', null=True, blank=True)
    exit_time = models.TimeField('Vrijeme izlaska', null=True, blank=True)
    flag = models.CharField('Vrsta rada', max_length=14, choices=FLAG_CHOICES, blank=True, null=True)
    processed = models.BooleanField('Potvrdi', default=False)

    class Meta:
        unique_together = ('worker', 'current_date')

    def __str__(self):
        return self.worker.name + ' ' + self.worker.surname + ' ' +  str(self.current_date) + ' ' + str(self.enter_time) + ' - ' + str(self.exit_time)

# load fixture sa ./manage.py loaddata data.json
class Marker(models.Model):
    value = models.IntegerField(default=0)