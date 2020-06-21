from django.contrib import admin

from testsuite.models import Test, Answers, Question


class QuestionInLine(admin.TabularInline):
    model = Question
    fields = ('text', 'number')
    show_change_link = True
    extra = 0


class TestAdminModel(admin.ModelAdmin):
    fields = ('title', 'description', 'level', 'image')
    list_display = ('title', 'description', 'level', 'image')
    list_per_page = 10
    inlines = (QuestionInLine, )


class AnswersInLine(admin.TabularInline):
    model = Answers
    fields = ('text', 'is_correct')
    show_change_link = True
    extra = 0


class QuestionsAdminModel(admin.ModelAdmin):
    fields = ('text',)
    list_display = ('text',)
    list_per_page = 10
    search_fields = ('first_name',)
    inlines = (AnswersInLine, )


admin.site.register(Test, TestAdminModel)
admin.site.register(Question, QuestionsAdminModel)
admin.site.register(Answers)
