from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum, Count, Q


class Topic(models.Model):

    title = models.CharField(max_length=64)
    description = models.TextField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class Test(models.Model):
    MIN_LIMIT = 3
    MAX_LIMIT = 20

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

    def questions_count(self):
        return self.questions.count()

    def last_run(self):
        last_run = self.test_result.order_by('-id').first()
        return last_run.datetime_run

    def best_result(self):
        best_res = self.test_result.order_by('-avr_score').first()
        return best_res.avr_score

    def num_of_runs(self):
        num_of_runs = self.test_result.order_by('id').count()
        return num_of_runs


class Question(models.Model):
    MIN_LIMIT = 3
    MAX_LIMIT = 20

    test = models.ForeignKey(to=Test, related_name='questions', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(MAX_LIMIT)],
                                              null=True)
    text = models.CharField(max_length=1024)
    description = models.TextField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f'{self.text}'


class Answers(models.Model):
    text = models.CharField(max_length=1024)
    question = models.ForeignKey(to=Question, related_name='answers', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}  -  {self.is_correct}'


class TestResult(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='test_result', on_delete=models.CASCADE)
    test = models.ForeignKey(to=Test, related_name='test_result', on_delete=models.CASCADE)
    avr_score = models.DecimalField(max_digits=10, decimal_places=2, default=0.0,
                                    validators=[MinValueValidator(0), MaxValueValidator(100)])
    datetime_run = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)

    def update_score(self):
        qs = self.test_result_details.values('question').annotate(
            num_answers=Count('question'),
            points=Sum('is_correct')
        )

        self.avr_score = sum(
            int(entry['points']) / entry['num_answers']
            for entry in qs
        )

    def correct_answers_count(self):
        correct_answer = self.test_result_details.values('question').\
            annotate(num_answers=Count('question'), score=Sum('is_correct'))
        return sum(entry['num_answers'] == int(entry['score']) for entry in correct_answer)

    def finish(self):
        self.update_score()
        self.is_completed = True

    def percent_answers(self):
        questions = self.test.questions_count()
        answers = self.correct_answers_count()
        return f'{answers} of {questions} - {(answers / questions) * 100:.2f}%'


class TestResultDetails(models.Model):
    text = models.CharField(max_length=64, default=None, null=True)
    test_result = models.ForeignKey(to=TestResult, related_name='test_result_details', on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, related_name='test_result_details', on_delete=models.CASCADE)
    answer = models.ForeignKey(to=Answers, related_name='test_result_details', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'Test Run: {self.test_result.id}, Question: {self.question.text}, Success: {self.is_correct}'


class TestSale(models.Model):
    store_id = models.PositiveSmallIntegerField()
    sold_on = models.DateField(auto_now_add=True)
    sum = models.DecimalField(max_digits=6, decimal_places=2)
