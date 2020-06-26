from django.contrib import admin

from testsuite.forms import AnswerInlineFormSet, TestForm, QuestionsInlineFormSet, \
    QuestionInlineForm
from testsuite.models import Test, Answers, Question, TestResult


class QuestionInLine(admin.TabularInline):
    model = Question
    fields = ('text', 'number', )
    show_change_link = True
    extra = 0
    form = QuestionInlineForm
    formset = QuestionsInlineFormSet


class TestAdminModel(admin.ModelAdmin):
    fields = ('title', 'description', 'level', 'image')
    list_display = ('title', 'description', 'level', 'image')
    list_per_page = 10
    inlines = (QuestionInLine, )
    form = TestForm


class AnswersInLine(admin.TabularInline):
    model = Answers
    fields = ('text', 'is_correct',)
    show_change_link = True
    extra = 0
    formset = AnswerInlineFormSet


class QuestionsAdminModel(admin.ModelAdmin):
    list_display = ('number', 'text', 'description', 'test',)
    list_select_related = ('test', )
    list_per_page = 10
    search_fields = ('first_name',)
    inlines = (AnswersInLine, )


admin.site.register(Test, TestAdminModel)
admin.site.register(Question, QuestionsAdminModel)
admin.site.register(Answers)
admin.site.register(TestResult)
