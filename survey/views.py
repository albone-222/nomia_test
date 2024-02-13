import random
import string
from typing import Any
from django.db import connection
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .utils import check_answer, ParseRawData

from .models import Answer, Question, Survey, UserAnswer


class MainView(ListView):
    model = Survey
    template_name = 'index.html'
    context_object_name = 'surveys'
    extra_context = {'title': 'Опросы'}
    
    def get_queryset(self) -> QuerySet[Any]:
        """
        Return a QuerySet of all Survey objects ordered by their id.
        """
        return Survey.objects.filter(question__id__isnull=False).values('id', 'name', 'description').annotate(qcount=Count('question')).order_by('id')
    
    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     # context['question_count'] = Question.objects.filter(survey=self.object.id).filter()
    #     return context
    
class SurveyView(DetailView):
    model = Survey
    template_name = 'survey.html'
    context_object_name = 'survey'
    pk_url_kwarg = 'survey_id'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Get the context data for the view.
        
        Args:
            **kwargs (Any): Additional keyword arguments.
        
        Returns:
            dict[str, Any]: The context data for the view.
        """
        context = super().get_context_data(**kwargs)
        context['question'] = Question.objects.filter(survey=self.object.id).filter(parents__isnull=True).first()
        return context

# class QuestionView(DetailView):
#     model = Question
#     template_name = 'question.html'
#     context_object_name = 'question'
#     pk_url_kwarg = 'question_id'
#     # pk_url_kwarg = 'question_id'
#     # print(pk_url_kwarg)
    
#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context['answers'] = Answer.objects.filter(owner=self.object.id).count()
#         return 

def question_view(request, survey_id, question_id):
    if request.user.is_anonymous:
        request.session['cached_session_key'] = request.session.session_key
    question = Question.objects.get(id=question_id)
    if question.survey.id != survey_id:
        return HttpResponse(status=404)
    print(request.session.session_key)
    context = {
        'question': question,
        'answers': Answer.objects.filter(owner=question.id).all(),
        'input': ''
    }
    return render(request, 'question.html', context)

def answer_view(request, survey_id, question_id):
    # print(request.GET)
    # print(request.COOKIES)
    answer = check_answer(request.GET['answer'], Answer.objects.filter(owner=question_id).all(), question_id)
    # print(answer.verify)
    user_answer = UserAnswer(session = request.COOKIES['sessionid'],
                             survey = Survey.objects.get(id = survey_id),
                             question = Question.objects.get(id = question_id),
                             answer = answer)
    user_answer.save()
    if answer.child:
        return redirect('question', survey_id, answer.child.id)
    
    request.session.create()
    return redirect('index')
    # return redirect('result', survey_id)
    
def result(request, survey_id):
    question_info_sql = f'''WITH stat_a AS (
                            SELECT answer_id AS id,
                                COUNT(DISTINCT session) AS a_count
                            FROM survey_useranswer
                            GROUP BY answer_id
                            ), stat_q AS (
                            SELECT question_id AS id,
                                COUNT(DISTINCT session) AS q_count,
                                DENSE_RANK() OVER (ORDER BY COUNT(DISTINCT session) DESC) AS number
                            FROM survey_useranswer
                            GROUP BY question_id
                            )
                            SELECT survey_answer.id AS id,
                                survey_typeverificationanswer.type_verification AS a_check,
                                survey_answer.text AS a_text,
                                stat_a.a_count,
                                survey_survey.name AS s_name,
                                survey_question.id AS q_id,
                                survey_question.text AS q_text,
                                stat_q.q_count,
                                stat_q.number,
                                (SELECT COUNT(DISTINCT session) FROM survey_useranswer) AS all_users_count
                            FROM survey_answer
                            LEFT JOIN stat_a ON stat_a.id=survey_answer.id
                            LEFT JOIN survey_verificationanswer ON survey_verificationanswer.id=survey_answer.verify_id
                            LEFT JOIN survey_typeverificationanswer ON survey_typeverificationanswer.id=survey_verificationanswer.type_verification_id
                            LEFT JOIN survey_question ON survey_question.id=survey_answer.owner_id
                            LEFT JOIN survey_survey ON survey_survey.id=survey_question.survey_id
                            LEFT JOIN stat_q ON stat_q.id=survey_answer.owner_id
                            WHERE survey_survey.id=1
                            ORDER BY number'''
    with connection.cursor() as cursor:
        cursor.execute(question_info_sql)
        raw_data = cursor.fetchall()
    parse_date = ParseRawData(raw_data)
    return render(request, 'result.html', parse_date.get_context())
