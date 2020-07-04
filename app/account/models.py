from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Max, Sum


class User(AbstractUser):
    image = models.ImageField(default='default.jpg', upload_to='pics')
    avr_score = models.PositiveIntegerField(null=True, blank=True)
    tests_list_passed = models.PositiveIntegerField(null=True, blank=True)

    def update_score(self):
        score = self.test_result.values('avr_score').\
            annotate(points=Sum('avr_score'))
        self.avr_score = sum(int(x['points']) for x in score)

    def test_last_run(self):
        last_run = self.test_result.order_by('-id').first()
        return last_run.datetime_run

    def percent(self):
        max_score = Max(self.avr_score)
        new = self.avr_score / max_score
        return new
