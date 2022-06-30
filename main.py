# -*- coding: utf-8 -*- 
import os
from datapreprocess import preprocess
import train_eval
import fire
from QA_data import QA_test
from config import Config
from bottle import get, post, request, Bottle, run, template, view

chatBot = Bottle()

@chatBot.get('/askme')
def login():
    return '''
        <head>
            <meta charset="UTF-8">
        </head>
        <form action="/askme" method="post">
            可以用中文问我一点问题: <input name="Question" type="text" />
            <input value="确定" type="submit" />
        </form>
    '''


@chatBot.post('/askme') # or @route('/login', method='POST')
@view('answer_template')
def do_login():
    
    Question = request.forms.Question

    if Question is None:
        return "请重新输入一个问题"
    else:
        
        (question_token, output_question, output_answer) = call_bot(str(Question))
        
        return {'Question':Question,
                'question_token':str(question_token),
                'output_question':output_question,
                'output_answer':output_answer}

        
        




def call_bot(input_sentence):

    match_outcome = QA_test.match(input_sentence)
    question_token = match_outcome["question_list"]
    query_res = match_outcome["answer_tuple"]
    
    if(query_res == tuple()):
        output_question = "没有在知识库中找到您想问的问题，会自动生成回答。"
        output_answer = train_eval.output_answer(input_sentence, searcher, sos, eos, unknown, opt, word2ix, ix2word)
    else:
        output_question = query_res[1]
        output_answer = query_res[2]
    
    return (question_token, output_question, output_answer)



# def chat(**kwargs):
    
#     opt = Config()
#     for k, v in kwargs.items(): #设置参数
#         setattr(opt, k, v)   

#     searcher, sos, eos, unknown, word2ix, ix2word = train_eval.test(opt)

#     if os.path.isfile(opt.corpus_data_path) == False:
#         preprocess()

#     while(1):
#         input_sentence = input('Ask Yanan > ')
#         if input_sentence == 'q' or input_sentence == 'quit' or input_sentence == 'exit': break
#         if opt.use_QA_first:
#             query_res = QA_test.match(input_sentence)
#             if(query_res == tuple()):
#                 output_answer = train_eval.output_answer(input_sentence, searcher, sos, eos, unknown, opt, word2ix, ix2word)
#             else:
#                 output_answer = "您是不是想问: " + query_res[1] + '\n问题的答案是: ' + query_res[2]
#         else:
#             output_answer = train_eval.output_answer(input_sentence, searcher, sos, eos, unknown, opt, word2ix, ix2word)
#         print('BOT > ',output_answer)

#     QA_test.conn.close()


if __name__ == "__main__":
    
    opt = Config()    
    opt.use_QA_first = True
    # searcher, sos, eos, unknown, word2ix, ix2word = train_eval.test(opt)
    searcher, sos, eos, unknown, word2ix, ix2word = train_eval.test(opt)


    # fire.Fire()
    run(chatBot, host='0.0.0.0', port=8081)


