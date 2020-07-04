import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView

from testsuite.models import Test, TestResult, Question, Answers, TestResultDetails


class TestListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = 'test_list.html'
    context_object_name = 'test_list'
    login_url = reverse_lazy('account:login')
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        return qs


class LeaderBoardView(LoginRequiredMixin, ListView):
    model = TestResult
    template_name = 'leader_list.html'
    context_object_name = 'leader_list'
    login_url = reverse_lazy('account:login')
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs


class TestRunView(View):
    PREFIX = 'answer_'

    def get(self, request, pk):
        if 'testresult' not in request.session:
            return HttpResponse('ERROR!')

        testresult_step = request.session.get('testresult_step', 1)
        request.session['testresult_step'] = testresult_step

        question = Question.objects.get(test__id=pk, number=testresult_step)

        answers = [answer.text for answer in question.answers.all()]

        return render(request=request,
                      template_name='test_run.html',
                      context={
                          'question': question,
                          'answers': answers,
                          'prefix': self.PREFIX
                      })

    def post(self, request, pk):
        if 'testresult_step' not in request.session:
            return HttpResponse('ERROR!')

        testresult_step = request.session['testresult_step']

        test = Test.objects.get(pk=pk)

        question = Question.objects.get(test__id=pk, number=testresult_step)

        answers = Answers.objects.filter(
            question=question
        ).all()

        choices = {
            k.replace(self.PREFIX, ''): True
            for k in request.POST if k.startswith(self.PREFIX)
        }

        if not choices:
            messages.error(self.request, extra_tags='danger', message="Error: You should select at least 1 answer")
            return redirect(reverse('test:next', kwargs={'pk': pk}))

        if len(choices) == len(answers):
            messages.error(self.request, extra_tags='danger', message="Error: You can't select ALL answers")
            return redirect(reverse('test:next', kwargs={'pk': pk}))

        current_test_result = TestResult.objects.get(
            id=request.session['testresult']
        )

        for idx, answer in enumerate(answers, 1):
            value = choices.get(str(idx), False)
            TestResultDetails.objects.create(
                test_result=current_test_result,
                question=question,
                answer=answer,
                is_correct=(value == answer.is_correct)
            )

        if question.number < test.questions_count():
            current_test_result.is_new = False
            current_test_result.save()
            request.session['testresult_step'] = testresult_step + 1
            return redirect(reverse('test:next', kwargs={'pk': pk}))
        else:
            del request.session['testresult']
            del request.session['testresult_step']
            current_test_result.finish()
            current_test_result.save()
            return render(
                request=request,
                template_name='testrun_end.html',
                context={
                    'test_result': current_test_result,
                    'time_spent': datetime.datetime.utcnow() - current_test_result.datetime_run.replace(tzinfo=None),
                }
            )


class StartTestView(View):

    def get(self, request, pk):
        test = Test.objects.get(pk=pk)

        test_result_id = request.session.get('testresult')

        if test_result_id:
            test_result = TestResult.objects.get(id=test_result_id)
        else:
            test_result = TestResult.objects.create(
                user=request.user,
                test=test
            )

        request.session['testresult'] = test_result.id

        return render(
            request=request,
            template_name='testrun_start.html',
            context={
                'test': test,
                'test_result': test_result
            },
        )
