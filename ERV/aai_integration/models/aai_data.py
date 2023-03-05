import datetime

from django.conf import settings
from django.db import models


class AAIData(models.Model):
    class AffiliationChoices(models.TextChoices):
        NONE = ''
        LIFELONG_LEARNING = 'cjeloživotno obrazovanje'
        EMPLOYEE = 'djelatnik'
        GUEST = 'gost'
        USER = 'korisnik usluge'
        STUDENT = 'student'
        PUPIL = 'učenik'
        EXTERNAL_ASSOCIATE = 'vanjski suradnik'

    class StaffCategoryChoices(models.TextChoices):
        NONE = ''
        ADMINISTRATIVE_STAFF = 'administrativno osoblje'
        ICT_SUPPORT = 'ICT podrška'
        RESEARCHERS = 'istraživači'
        TEACHING_STAFF = 'nastavno osoblje'
        LIBRARY_STAFF = 'osoblje knjižnice'
        TECHNICAL_STAFF = 'tehničko osoblje'

    class StudentCategoryChoices(models.TextChoices):
        NONE = ''
        PRIMARY = 'osnovnoškolac'
        SECONDARY = 'srednjoškolac'
        PART_TIME_PRE_BOLOGNA_UNDERGRADUATE = 'izvanredni student:pred-bolonjski studij'
        PART_TIME_UNDERGRADUATE = 'izvanredni student:preddiplomski sveučilišni studij'
        PART_TIME_PROFESSIONAL_UNDERGRADUATE = 'izvanredni student:preddiplomski stručni studij'
        PART_TIME_GRADUATE = 'izvanredni student:diplomski sveučilišni studij'
        PART_TIME_SPECIALIST_PROFESSIONAL_GRADUATE = 'izvanredni student:specijalistički diplomski stručni studij'
        PART_TIME_INTEGRATED = 'izvanredni student:integrirani studij'
        PART_TIME_SPECIALIST_POST_GRADUATE = 'izvanredni student:specijalistički poslijediplomski studij'
        PART_TIME_PHD = 'izvanredni student:doktorski studij'
        FULL_TIME_PRE_BOLOGNA_UNDERGRADUATE = 'redoviti student:pred-bolonjski studij'
        FULL_TIME_UNDERGRADUATE = 'redoviti student:preddiplomski sveučilišni studij'
        FULL_TIME_PROFESSIONAL_UNDERGRADUATE = 'redoviti student:preddiplomski stručni studij'
        FULL_TIME_GRADUATE = 'redoviti student:diplomski sveučilišni studij'
        FULL_TIME_SPECIALIST_PROFESSIONAL_GRADUATE = 'redoviti student:specijalistički diplomski stručni studij'
        FULL_TIME_INTEGRATED = 'redoviti student:integrirani studij'
        FULL_TIME_SPECIALIST_POST_GRADUATE = 'redoviti student:specijalistički poslijediplomski studij'
        FULL_TIME_PHD = 'redoviti student:doktorski studij'
        DORMANT = 'mirovanje statusa studenta'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE,
                                related_name=getattr(settings, 'AAI_DATA_RELATED_NAME', 'aai_data'))
    organization_name = models.CharField(max_length=200, default='')
    primary_affiliation = models.CharField(choices=AffiliationChoices.choices, max_length=24,
                                           default=AffiliationChoices.NONE)
    affiliation_expiration_date = models.CharField(max_length=8, default='NONE')
    staff_category = models.CharField(choices=StaffCategoryChoices.choices, max_length=23,
                                      default=StaffCategoryChoices.NONE)
    student_category = models.CharField(choices=StudentCategoryChoices.choices, max_length=59,
                                        default=StudentCategoryChoices.NONE)

    def get_affiliation_expiration_date(self):
        if self.affiliation_expiration_date != 'NONE':
            date = datetime.date(
                int(self.affiliation_expiration_date[:4]),
                int(self.affiliation_expiration_date[4:6]),
                int(self.affiliation_expiration_date[6:8])
            )
        else:
            date = None

        return date

    @property
    def affiliation_expired(self):
        expiration_date = self.get_affiliation_expiration_date()
        return self.get_affiliation_expiration_date() >= datetime.date.today() if expiration_date else False
