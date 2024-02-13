from django.urls import path

from .views import MainView, SurveyView, question_view, answer_view, result
urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('survey/<int:survey_id>/', SurveyView.as_view(), name='survey'),
    path('survey/<int:survey_id>/question/<int:question_id>/', question_view, name='question'),
    path('survey/<int:survey_id>/question/<int:question_id>/answer/', answer_view, name='answer'),
    path('survey/<int:survey_id>/result/', result, name='result'),
]