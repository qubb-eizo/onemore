from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from django.urls import reverse
from django.test import TestCase
from django.test import Client

from testsuite.models import Test, TestResult

PK = 1


class BaseFlowTest(TestCase):

    def setUp(self):
        call_command('loaddata', 'tests/fixtures/accounts.json', verbosity=0)
        call_command('loaddata', 'tests/fixtures/tests.json', verbosity=0)
        self.client = Client()
        self.client.login(username='qubb123', password='qubb123')

    def test_basic_flow(self):
        response = self.client.get(reverse('test:start', kwargs={'pk': PK}))
        assert response.status_code == 200
        assert 'START ▶️' in response.content.decode()

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        url = reverse('test:next', kwargs={'pk': PK})

        for step in range(1, questions_count + 1):
            response = self.client.get(url)
            assert response.status_code == 200
            assert 'Submit' in response.content.decode()
            response = self.client.post(
                path=url,
                data={
                    'answer_1': "1"
                }
            )
            if step < questions_count:
                self.assertRedirects(response, url)
            else:
                assert response.status_code == 200

        assert 'START ANOTHER TEST ▶️' in response.content.decode()

    def test_success_passed(self):
        response = self.client.get(reverse('test:start', kwargs={'pk': PK}))
        assert response.status_code == 200
        assert 'START ▶️' in response.content.decode()

        test = Test.objects.get(pk=PK)
        questions = test.questions.all()
        url = reverse('test:next', kwargs={'pk': PK})

        for idx, question in enumerate(questions, 1):
            response = self.client.get(url)
            assert response.status_code == 200
            assert 'Submit' in response.content.decode()

            correct_answers = {
                f'answer_{idx}': 1
                for idx, answer in enumerate(question.answers.all(), 1)
                if answer.is_correct
            }

            response = self.client.post(
                path=url, data=correct_answers
            )

        test_result = TestResult.objects.order_by('id').last()
        assert 'START ANOTHER TEST ▶️' in response.content.decode()
        self.assertEqual(test.questions_count(), float(test_result.avr_score))

    def test_failed(self):
        response = self.client.get(reverse('test:start', kwargs={'pk': PK}))
        assert response.status_code == 200
        assert 'START ▶️' in response.content.decode()

        test = Test.objects.get(pk=PK)
        questions = test.questions.all()
        url = reverse('test:next', kwargs={'pk': PK})

        for idx, question in enumerate(questions, 1):
            response = self.client.get(url)
            assert response.status_code == 200
            assert 'Submit' in response.content.decode()

            correct_answers = {
                f'answer_{idx}': 0
                for idx, answer in enumerate(question.answers.all(), 1)
                if not answer.is_correct
            }

            response = self.client.post(
                path=url, data=correct_answers
            )

        assert 'START ANOTHER TEST ▶️' in response.content.decode()
