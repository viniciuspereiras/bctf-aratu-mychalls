from flask import Flask, render_template, request, make_response, redirect, \
session
from captcha.image import ImageCaptcha

import random
import string
import os
import json
import base64 

def randomize():
    char_set = string.ascii_lowercase + string.digits
    return ''.join(random.sample(char_set*6, 6))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'q!HsCyLoNed7a@#4iRytU*2aDWPB%5H9aL7fLz#g29rt9U4Cfb@%w^&PnJe2SdPSJtwUZvcF4@EACxeTL5ixYCLqw#TfSW63un9vRjxSp2f!FDQv49Z7awi3UFox9B7p'


@app.route('/', methods=['GET', 'POST'])
def template_test():
    image = ImageCaptcha(width=280, height=90)
    
    if request.method == 'POST':
        user_input = request.form.get('response')
        valid_captcha = session['last']


        if len(user_input) < 1:
            pass
        elif user_input != valid_captcha:
            if int(session['score']) > int(session['record']):
                session['record'] = session['score']
            session['score'] = 0
            session['message'] = 'GAME OVER, try again... :/'
        elif len(valid_captcha) > 1 and user_input == valid_captcha:
            session['score'] = int(session['score']) + 1
            session['message'] = ''
    try:
        os.remove('static/captcha.png')
    except:
        pass

    payload = randomize()
    image.write(payload, 'static/captcha.png')
    
    session['last'] = str(payload)
    
    if 'score' not in session:
        session['score'] = 0
        session['message'] = ''
    if 'record' not in session:
        session['record'] = 0
    if 'last' not in session:
        session['last'] = 'big0us'
    
    if int(session['score']) >= 1000:
        session['message'] = 'bCTF{60e01ab8b0d203cb8cfa2e5b1e4cd23d}'
        

    return render_template('template.html', score=str(session['score']), record=str(session['record']), message=session['message'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)