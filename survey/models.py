from typing import Any
from django.db import models

class Survey(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default='Test')
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Опросы"
        verbose_name = "Опросы"


        
class Question(models.Model):
    text = models.CharField(max_length=200, verbose_name = 'Вопрос')
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, verbose_name = 'Опрос')
    type_answer = models.ForeignKey('TypeQuestion', on_delete=models.CASCADE, verbose_name = 'Тип ответа', blank=True, default = 1)
    
    def __str__(self) -> str:
        return self.text
    
    class Meta:
        verbose_name = "Вопросы"
        verbose_name_plural = "Вопросы"

class Answer(models.Model):
    owner = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers', verbose_name = 'Вопрос')
    text = models.CharField(max_length=200, verbose_name = 'Ответ')
    child = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='parents', verbose_name = 'Следующий вопрос', null=True, blank=True)
    verify = models.ForeignKey('VerificationAnswer', on_delete=models.CASCADE, verbose_name = 'Тип сопоставления', blank=True, default = 1)
    def __str__(self) -> str:
        return f'{self.owner} - {self.text}'
    class Meta:
        verbose_name_plural = "Ответы"
        verbose_name = "Ответы"

class TypeQuestion(models.Model):
    type_question = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.type_question
    
class TypeVerificationAnswer(models.Model):
    type_verification = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.type_verification

class VerificationAnswer(models.Model):
    type_question = models.ForeignKey('TypeQuestion', on_delete=models.CASCADE, verbose_name = 'Тип вопроса')
    type_verification = models.ForeignKey('TypeVerificationAnswer', on_delete=models.CASCADE, verbose_name = 'Тип сопоставления')
    def __str__(self) -> str:
        return f'{self.type_question} - {self.type_verification}'
    
class UserAnswer(models.Model):
    session = models.CharField(max_length=200)
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, verbose_name = 'Опрос')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name = 'Вопрос')
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, verbose_name = 'Ответ')