from django.contrib import admin

from .models import Question, Choice, Answer

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['question_text']


class AnswerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user', 'question', 'answer_self', 'answer_other', 'importance', 'public_self', 'public_other']}),
        ('Date information', {'fields': ['answer_date'], 'classes': ['collapse']}),
    ]
    list_display = ('user', 'public_self', 'public_other', 'answer_date')
    list_filter = ['answer_date','user']
    search_fields = ['question']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)