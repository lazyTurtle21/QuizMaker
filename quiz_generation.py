from datetime import datetime
import random

def create_quiz_question(body, key, index, distractors=[], correct_answer=False):
    question = body.lower().replace(key, '_' * 10)
    options = distractors + [key]
    random.shuffle(options)
    
    question_body = f' {index} ' + question + '\n'
    for i, option in enumerate(options):
        question_body += f'({chr(97 + i)}) {option}\t' 
    
    if correct_answer:
        question_body += f'\n(Answer: {key})'
    return question_body
    
    
def create_quiz(questions, correct_answer=False, save=False):
    """
    [[body, key, distractors], ...], correct_answer -> quiz 
    """
    quiz = 'This is a LinearUp - automatically generated quiz\n\n\n'
    answers = 'answers for quiz:\n'
    index = 0
    for question in questions:
        if len(question) < 2:
            raise ValueError('Need to pass at least question and key')
        quiz += create_quiz_question(
            body=question[0], 
            key=question[1], 
            index=index,
            distractors=[] if len(question) == 2 else question[2], 
            correct_answer=correct_answer
        ) + '\n\n'
        answers += " {} ".format(index) + question[1] + "\n"
        index += 1
    if save:
        with open("generated_quizzes/" + f"quiz_{int(datetime.now().timestamp())}.txt", "w") as text_file:
            text_file.write(quiz)
        with open("generated_quizzes/" + f"answers_{int(datetime.now().timestamp())}.txt", "w") as text_file:
            text_file.write(answers)

    return quiz