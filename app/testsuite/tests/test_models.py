import datetime

from django.core.management import call_command
from django.test import TestCase

from testsuite.models import Test, Question


class TestModelTest(TestCase):

    def setUp(self):
        call_command('loaddata', 'tests/fixtures/accounts.json', verbosity=0)
        call_command('loaddata', 'tests/fixtures/tests.json', verbosity=0)

    def tearDown(self):
        pass

    def test_questions_count(self):
        test = Test.objects.first()
        count = test.questions_count()
        question = Question.objects.create(
            test=test, number=1,
            text='Question text'
        )
        self.assertEqual(test.questions_count(), count + 1)

    def test_last_run(self):
        call_command('loaddata', 'tests/fixtures/accounts.json', verbosity=0)
        call_command('loaddata', 'tests/fixtures/tests.json', verbosity=0)

        test = Test.objects.first()
        dt = datetime.datetime.strptime('2020-07-04T09:50:06.593Z', "%Y-%m-%dT%H:%M:%S.%f%z")
        self.assertEqual(test.last_run(), dt)
