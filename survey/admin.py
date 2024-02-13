from django.contrib import admin

from .models import Survey, Question, Answer, VerificationAnswer

admin.site.register(Survey)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'survey')
    list_filter = ('survey',)
    

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('owner', 'text', 'child')
    list_filter = ('owner',)