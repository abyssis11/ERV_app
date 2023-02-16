from django.db import models
from datetime import date, datetime 

DESCRIPTION_CHOICES = {
    ('administracija', 'administracija'),
    ('nastavnici', 'nastavnici')
}


class Job(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=15, choices=DESCRIPTION_CHOICES)
   
    def __str__(self):
        return self.name

class Worker(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    job = models.ForeignKey(Job, on_delete=models.CASCADE) 


    def __str__(self):
        return self.name + ' ' + self.surname

class ExitReadValue(models.Model):
    current_day = models.DateField(default=date.today)
    current_time = models.TimeField()
    building = models.CharField(max_length=50)
   
    def __str__(self):
        return str(self.current_day) + ' ' + str(self.current_time)

class EnterReadValue(models.Model):
    current_day = models.DateField(default=date.today, null=True, blank=True)
    current_time = models.TimeField(null=True, blank=True)
    building = models.CharField(max_length=50, null=True, blank=True)
   
    def __str__(self):
        return str(self.current_day) + ' ' + str(self.current_time) 

class ERV(models.Model):
    delta_time = models.TimeField()
    flag = models.CharField(max_length=2)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    enter_read_value = models.OneToOneField(EnterReadValue, on_delete=models.CASCADE, null=True, blank=True)
    exit_read_value = models.OneToOneField(ExitReadValue, on_delete=models.CASCADE, null = True)
    def __str__(self):
        return self.worker.name + ' ' + self.worker.surname + ' ' + str(self.enter_read_value.current_day) + ' ' + str(self.enter_read_value.current_time) + ' - ' + str(self.exit_read_value.current_time)
