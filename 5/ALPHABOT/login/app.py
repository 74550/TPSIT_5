
import AlphaBot
import time
from flask import Flask, render_template, redirect, url_for, request
import sqlite3
from random import randint
n = 6

IP_ROBOT='0.0.0.0'

app = Flask(__name__)

r=AlphaBot.AlphaBot()

def validate(username, password):
    completion = False
    con = sqlite3.connect('./db.db')
    #with sqlite3.connect('static/db.db') as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser==username:
            completion=check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            global url_n
            url_n = randint(1,1234567890)
            return redirect(url_for(f'secret'))
    return render_template('login.html', error=error)

@app.route('/secret', methods=['GET', 'POST'])
def secret():
    if request.method == 'POST':
        print(request.form.get('action1'))
        if request.form.get('action1') == 'Forward':
            r.backward()
            time.sleep(2)
            r.stop()
        elif  request.form.get('action2') == 'Backward':
            r.forward()
            time.sleep(2)
            r.stop()
        elif  request.form.get('action3') == 'Right':
            r.right()
            time.sleep(2)
            r.stop()
        elif  request.form.get('action4') == 'Left':
            r.left()
            time.sleep(2)
            r.stop()
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")

if __name__== "__main__":
    app.run(debug=True, host=IP_ROBOT, port=8000)