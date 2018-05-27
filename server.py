import json
import os
from flask import Flask, redirect, render_template, request, url_for, \
    send_from_directory
from alchemy_postgresql import messageToDb, messagesFromDb, selectDbTable, \
    delMessages
from unique import getCountOfUniqueWords

app = Flask(__name__)

table = selectDbTable()
# delMessages(table)


@app.route('/send')
def send():
    return render_template('send.html')


@app.route('/upload', methods=['POST'])
def upload():
    try:
        message = request.form['input-text']
        messageToDb(table, message, getCountOfUniqueWords(message))
        return json.dumps(1), 200
    except Exception:
        return json.dumps(0), 500


@app.route('/result')
def result():
    messages = messagesFromDb(table)
    return render_template('result.html', text=messages)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('send'))

if __name__ == '__main__':
    app.run(port=7777, debug=True)
