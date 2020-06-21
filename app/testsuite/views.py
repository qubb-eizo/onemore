from django.views.generic import ListView

from testsuite.models import Test, TestResult


class TestListView(ListView):
    model = Test
    template_name = 'test_list.html'
    context_object_name = 'test_list'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Test list'
        return context


class LeaderBoardView(ListView):
    model = TestResult
    template_name = 'leader_list.html'
    context_object_name = 'leader_list'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Leader list'
        return context
