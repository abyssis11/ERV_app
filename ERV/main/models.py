from django.db import models
from datetime import date, datetime 

CATEGORY_CHOICES = {
    ('Administracija', 'Administracija'),
    ('Nastavnici', 'Nastavnici')
}

FLAG_CHOICES = {
    ('Redovni rad', 'Redovni rad'),
    ('Putni nalog', 'Putni nalog'),
    ('Bolovanje', 'Bolovanje'),
    ('Slobodan dan', 'Slobodan dan'),
    ('Godišnji odmor', 'Godišnji odmor'),
    ('Rad od kuće', 'Rad od kuće')
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
    current_date = models.DateField('Razdoblje', default=date.today)
    enter_time = models.TimeField('Vrijeme ulaska', null=True, blank=True)
    exit_time = models.TimeField('Vrijeme izlaska', null=True, blank=True)
    delta_time = models.TimeField('Vrijeme rada', null=True, blank=True)
    flag = models.CharField('Vrsta rada', max_length=14, choices=FLAG_CHOICES, blank=True, null=True)
    processed = models.BooleanField('Potvrdi', default=False)

    class Meta:
        unique_together = ('worker', 'current_date')
        ordering = ['-current_date']

    def save(self, *args, **kwargs):
        FORMAT_TIME = '%H:%M:%S'
        if self.enter_time != None and self.exit_time != None:
            exit = datetime.combine(self.current_date, self.exit_time)
            enter = datetime.combine(self.current_date, self.enter_time)
            delta = str(exit - enter)
            self.delta_time = datetime.strptime(delta, FORMAT_TIME)
        super(ERV, self).save(*args, **kwargs)

    def __str__(self):
        return self.worker.name + ' ' + self.worker.surname + ' ' +  str(self.current_date) + ' ' + str(self.enter_time) + ' - ' + str(self.exit_time)

# load fixture sa ./manage.py loaddata data.json
class Marker(models.Model):
    value = models.IntegerField(default=0)

"""     def save(self, *args, **kwargs):
        created = self.pk is None
        super(ERV, self).save(*args, **kwargs)
        print('save')
        if created and self.enter_time != None and self.exit_time != None:
            print('deltaTime')
            print(self.enter_time)
            print(self.exit_time)
            self.delta_time = self.exit_time - self.enter_time   """