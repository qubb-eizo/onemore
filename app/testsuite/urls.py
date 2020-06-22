from django.urls import path

from testsuite.views import LeaderBoardView, TestListView

app_name = 'testsuite'

urlpatterns = [
    path('list/', TestListView.as_view(), name='test_list'),
    path('leader_board/', LeaderBoardView.as_view(), name='leader_list'),
]
