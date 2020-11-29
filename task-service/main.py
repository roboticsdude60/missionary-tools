"""Cloud Task workers"""
import json
import logging
from multiprocessing import Process

#import google.cloud.logging
from flask import Flask, request, send_from_directory

from missionary_bot import MissionaryBot

app = Flask(__name__)
#client = google.cloud.logging.Client()
#client.get_default_handler()
#client.setup_logging()

def do_work(kwargs):
    MissionaryBot(**kwargs).do_work()

@app.route('/find_member_profiles', methods=['POST'])
def find_member_profiles():
    """Log the request payload."""
    payload = request.get_data(as_text=True) or '(empty payload)'
    try:
        p = Process(target=do_work, args=(json.loads(payload),)) #TODO Give the theads and processes names
        p.start()
        return "Started process"
    except Exception as e:
        logging.error(e)
        return f"{e} Didn't completed loading Facebook profile information"
    return "Completed loading Facebook profile information"

@app.route('/')
def hello():
    """Basic index to verify app is serving."""
    return 'Hello World!'


@app.route('/liveness_check')
def liveness_check():
    return "OK"

@app.route('/readiness_check')
def readiness_check():
    return "OK"

@app.route('/debug/<path:path>')
def send_assets(path):
    return send_from_directory('debug', path)

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', port=5000, debug=True)