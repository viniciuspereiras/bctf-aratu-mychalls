import re
from flask import Flask
from flask import render_template, request
from werkzeug.utils import redirect
import jwt
import json
import base64

SECRET_KEY = 'Exit-Tranquil-Hypnotist-Slam-Shredder0-Depose-Eggshell-Laxative-Onion-Crafty'

def gen_jwt(username, secret):
    return jwt.encode({'username': username}, secret, algorithm='HS256')

def verify_jwt(jwt_token, secret):
    token_b64 = jwt_token.replace('-', '+').replace('_', '/')
    try:
        header = json.loads(base64.b64decode(token_b64.split('.')[0] + "==="))
    except Exception as e:
        return "error"

    if "alg" in header:
        algorithm = header["alg"]

    if algorithm == "HS256":
        try:
            decoded = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
            return decoded.get('username')
        except Exception as e:
            return "error"
    
    elif algorithm == "none":
        try:
            decoded = jwt.decode(jwt_token, verify=False)
            return decoded.get('username')
        except Exception as e:
            return "error"
    else:
        return "error"


app = Flask(__name__)

@app.route('/')
def index():    
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin': ###senha
            resp = app.make_response(redirect('/panel'))
            resp.set_cookie('hmmmm_cookies', gen_jwt(username, SECRET_KEY))
            return resp
        else:
            print('wrong')
            return render_template('login.html', message='Wrong username or password')
    else:
        print('ajkhjkllklkj')
        return render_template('login.html')


@app.route('/panel')
def panel():    
    cookie = request.cookies.get('hmmmm_cookies')
    if cookie:
        username = verify_jwt(cookie, SECRET_KEY)
        print(f'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa{username}')
        try:
            with open(f'static/{username}.png', "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                print(encoded_string)
                return render_template('panel.html', base64content=encoded_string.decode('utf-8'))
        except FileNotFoundError:
            try:
                with open(f'static/{username}', "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                    print(encoded_string)
                    return render_template('panel.html', base64content=encoded_string.decode('utf-8'))
            except:
                return render_template('panel.html', message='No image file found')
    else:
        return redirect('/login')
   

@app.route('/logout')
def logout():
    resp = app.make_response(redirect('/login'))
    resp.set_cookie('hmmmm_cookies', '', expires=0)
    return resp 

app.run(host='0.0.0.0', port=5000)
