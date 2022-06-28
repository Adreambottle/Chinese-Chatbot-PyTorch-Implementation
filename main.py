# -*- coding: utf-8 -*- 
import os
from datapreprocess import preprocess
import train_eval
import fire
from QA_data import QA_test
from config import Config
from bottle import get, post, request, Bottle, run, template

chatBot = Bottle()

@chatBot.get('/askme')
def login():
    return '''
        <form action="/askme" method="post">
            Ask me something: <input name="Question" type="text" />
            <input value="确定" type="submit" />
        </form>
    '''

@chatBot.post('/askme') # or @route('/login', method='POST')
def do_login():
    Question = request.forms.get('Question')

    if Question is None:
        return "<p>Please input somthing</p>"
    else:
        output_words = call_bot(Question)
        
        answer = template('回答是：{{output_words}}', output_words=output_words)
        return answer




def call_bot(input_sentence):
    opt = Config()
    opt.use_QA_first = True

    searcher, sos, eos, unknown, word2ix, ix2word = train_eval.test(opt)

    if os.path.isfile(opt.corpus_data_path) == False:
        preprocess()
    
    query_res = QA_test.match(input_sentence)
    if(query_res == tuple()):
        output_words = train_eval.output_answer(input_sentence, searcher, sos, eos, unknown, opt, word2ix, ix2word)
    else:
        output_words = "您是不是要找以下问题: " + query_res[1] + '，您可以尝试这样: ' + query_res[2]
    # QA_test.conn.close()
    return output_words


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
#                 output_words = train_eval.output_answer(input_sentence, searcher, sos, eos, unknown, opt, word2ix, ix2word)
#             else:
#                 output_words = "您是不是要找以下问题: " + query_res[1] + '，您可以尝试这样: ' + query_res[2]
#         else:
#             output_words = train_eval.output_answer(input_sentence, searcher, sos, eos, unknown, opt, word2ix, ix2word)
#         print('BOT > ',output_words)

#     QA_test.conn.close()


if __name__ == "__main__":
    # fire.Fire()
    run(chatBot, host='localhost', port=8081)

