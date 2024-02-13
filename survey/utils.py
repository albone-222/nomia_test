from typing import List

from .models import Answer, Question


def check_answer(user_answer: str, answers: List[Answer], question_id: int) -> bool:
    question_type = Question.objects.get(id=question_id).type_answer
    print(question_type)
    for answer in answers:
        print(answer)
        if str(answer.verify.type_verification) == 'Равно':
            print('проверка равно')
            if check_equals(user_answer, answer.text):
                return answer
        elif str(answer.verify.type_verification) == 'Не равно':
            print('проверка не равно')
            if not check_equals(user_answer, answer.text):
                return answer
        elif str(answer.verify.type_verification) == 'Содержит':
            print('проверка содержит')
            if check_contains(user_answer, answer.text):
                return answer
        elif str(answer.verify.type_verification) == 'Не содержит':
            print('проверка не содержит')
            if not check_contains(user_answer, answer.text):
                return answer
        elif str(answer.verify.type_verification) == 'Больше или равно':
            print('больше или равно')
            if check_gt(user_answer, answer.text, str(question_type)) or check_equals(user_answer, answer.text):
                return answer
        elif str(answer.verify.type_verification) == 'Больше чем':
            print('больше чем')
            if check_gt(user_answer, answer.text, question_type):
                return answer
        elif str(answer.verify.type_verification) == 'Меньше или равно':
            print('меньше или равно')
            if check_lt(user_answer, answer.text, str(question_type)) or check_equals(user_answer, answer.text):
                return answer
        elif str(answer.verify.type_verification) == 'Меньше чем':
            print('меньше чем')
            if check_lt(user_answer, answer.text, str(question_type)):
                return answer
        elif str(answer.verify.type_verification) == 'Между (включая левую и не включая правую)':
            print('между')
            if check_between(user_answer, answer.text):
                return answer
        elif str(answer.verify.type_verification) == 'Не между (диапазон включает левую и не включает правую)':
            print('не между')
            if not check_between(user_answer, answer.text):
                return answer

def check_equals(user_answer: str, answer: str):
    return user_answer.lower() == answer.lower()

def check_contains(user_answer: str, answer: str):
    return answer.lower() in user_answer.lower()

def check_gt(user_answer: str, answer: str, question_type: int):
    if question_type == 'Выбор ответа, возможен выбор нескольких':
        return len(user_answer) > len(answer)
    elif question_type == 'Свободный ввод числа':
        print('проверка тестового ввода числа больше чем')
        print(float(user_answer) > float(answer))
        return float(user_answer) > float(answer)
    else:
        return len(user_answer) > int(answer)
    
def check_lt(user_answer: str, answer: str, question_type: int):
    if question_type == 'Выбор ответа, возможен выбор нескольких':
        return len(user_answer) < len(answer)
    elif question_type == 'Свободный ввод числа':
        print('проверка тестового ввода числа меньше чем')
        print(float(user_answer) < float(answer))
        return float(user_answer) < float(answer)
    else:
        return len(user_answer) < int(answer)

def check_between(user_answer: str, answer: str):
    return float(user_answer) >= int(answer.split(' ')[0]) and int(user_answer) < int(answer.split(' ')[1])

class ParseRawData():
    def __init__(self, data):
        self.data = data
        self.survey_name = self.get_survey_name()
        self.question_dict = self.get_questions()
        self.answer_dict = self.get_answers()
        self.all_users_count = self.get_all_users_count()
        
    def get_survey_name(self):
        return self.data[0][4]
    
    def get_all_users_count(self):
        return self.data[0][9]
    
    def get_questions(self):
        question_dict = {}
        for row in self.data:
            if row[5] not in question_dict.keys():
                question_dict[row[5]] = {'id': row[5],
                                         'text': row[6],
                                         'question_count': row[7] or 0,
                                         'number': row[8],
                                         'percent': (row[7] or 0)*100/row[9]}
        return question_dict
        
    def get_answers(self):
        answer_dict = {}
        for row in self.data:
            if row[0] not in answer_dict.keys():
                answer_dict[row[0]] = {'id': row[0],
                                       'text': f'{row[1]} {row[2]}',
                                       'answer_count': row[3] or 0,
                                       'percent': (row[3] or 0)*100/row[9],
                                       'question': row[5]}
        return answer_dict
    
    def get_context(self):
        return {'users_count': self.all_users_count,
                'survey': self.survey_name,
                'questions': self.question_dict.values(),
                'answers': self.answer_dict.values()
                }