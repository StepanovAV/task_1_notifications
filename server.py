import os
import json
from run import *
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
    send_from_directory,
)
from alchemy_postgresql import (
    message_to_db,
    messages_from_db,
    select_db_table
)
from sqlalchemy.exc import OperationalError 
from unique import count_of_unique_words

app = Flask(__name__)


@app.route('/send')
def send():
    return render_template('send.html')


@app.route('/upload', methods=['POST'])
def upload():
    try:
        message = request.form['input-text']
        message_to_db(message, count_of_unique_words(message))
        return json.dumps(1), 200
    except OperationalError:
        return json.dumps('OperationalError'), 500


@app.route('/result')
def result():
    try:
        messages = messages_from_db()
    except OperationalError:
        messages = [['Database problem, try later', '']]
    return render_template('result.html', text=messages)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('send'))

if __name__ == '__main__':
    port = os.environ['NOTIFICATIONS_APP_PORT']
    debug = os.environ['NOTIFICATIONS_APP_DEBUG'] == 'TRUE'
    app.run(port=port, host='0.0.0.0', debug=debug)
