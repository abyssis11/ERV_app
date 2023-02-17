from django.db import models
from datetime import date, datetime 

CATEGORY_CHOICES = {
    ('administracija', 'administracija'),
    ('nastavnici', 'nastavnici')
}

FLAG_CHOICES = {
    ('rednovni rad', 'RR'),
    ('putni nalog', 'PN'),
    ('bolovanje', 'BO'),
    ('slobodan dan', 'SL'),
    ('godisnji odmor', 'GO'),
    ('rad od kuce', 'RK')
}


class Job(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
   
    def __str__(self):
        return self.name

class Worker(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    job = models.ForeignKey(Job, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name + ' ' + self.surname


class ERV(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.DO_NOTHING) # on_delete=models.CASCADE
    current_date = models.DateField(default=date.today)
    enter_time = models.TimeField(null=True, blank=True)
    exit_time = models.TimeField(null=True, blank=True)
    flag = models.CharField(max_length=14, choices=FLAG_CHOICES)

    class Meta:
        unique_together = ('worker', 'current_date')

    def __str__(self):
        return self.worker.name + ' ' + self.worker.surname + ' ' +  str(self.current_date) + ' ' + str(self.enter_time) + ' - ' + str(self.exit_time)
