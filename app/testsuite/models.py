from django.conf import settings
from django.db import models


class Topic(models.Model):

    title = models.CharField(max_length=64)
    description = models.TextField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class Test(models.Model):
    LEVEL_CHOICES = (
        (1, 'Basic'),
        (2, 'Middle'),
        (3, 'Advanced')
    )

    topic = models.ForeignKey(to=Topic, related_name='tests', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=2048, null=True, blank=True)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=2)
    image = models.ImageField(default='default.png', upload_to='pics')

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    MIN_LIMIT = 3
    MAX_LIMIT = 6

    test = models.ForeignKey(to=Test, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f'{self.text}'


class Answers(models.Model):
    text = models.CharField(max_length=64)
    question = models.ForeignKey(to=Question, related_name='answers', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}  -  {self.is_correct}'


class TestResult(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='test_result', on_delete=models.CASCADE)
    test = models.ForeignKey(to=Test, related_name='test_result', on_delete=models.CASCADE)
    avr_score = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


class TestRunDetails(models.Model):
    test_result = models.ForeignKey(to=TestResult, related_name='test_run_details', on_delete=models.CASCADE)
    questions = models.ForeignKey(to=Question, related_name='test_run_details', on_delete=models.CASCADE)
    answers = models.ForeignKey(to=Answers, related_name='test_run_details', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
