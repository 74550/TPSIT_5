import AlphaBot
import time
from flask import Flask, render_template, request

IP_ROBOT='0.0.0.0'

app = Flask(__name__)

r=AlphaBot.AlphaBot()

@app.route("/", methods=['GET', 'POST'])
def index():
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

if __name__ == '__main__':
    app.run(debug=True, host=IP_ROBOT, port=8000)