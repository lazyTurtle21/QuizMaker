def create_quiz_question(body, key, distractors=[], correct_answer=False):
    question = body.replace(key, '_' * 10)
    options = distractors + [key]
    
    question_body = question + '\n'
    for i, option in enumerate(options):
        question_body += f'({chr(97 + i)}) {option}\t' 
    
    if correct_answer:
        question_body += f'\n(Answer:{key})'
    return question_body
    
    
def create_quiz(questions, correct_answer=False):
    """
    [[body, key, distractors], ...], correct_answer -> quiz 
    """
    quiz = 'This is a LinearUp - automatically generated quiz\n\n\n'
    for question in questions:
        if len(question) < 2:
            raise ValueError('Need to pass at least question and key')
        quiz += create_quiz_question(
            body=question[0], 
            key=question[1], 
            distractors=[] if len(question) == 2 else question[2], 
            correct_answer=correct_answer
        ) + '\n\n'
    
    return quiz