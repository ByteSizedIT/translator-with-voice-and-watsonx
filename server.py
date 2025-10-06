'''
# existing local venv: source ../3-simple-chatbot/.venv/bin/activate
# for new env: python -m venv .venv ; source .venv/bin/activate
echo $VIRTUAL_ENV - to checkwhich venv is running
'''

import base64
import json
from flask import Flask, render_template, request
from flask_cors import CORS
import os
from worker import speech_to_text, text_to_speech, watsonx_process_message

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    print("Processing speech-to-text")
    audio_binary = request.data # get the users speech from their request
    text = speech_to_text(audio_binary) # call speech-to-text fucntion to transcribe the audio 

    # return the response to the user in JSON format:  create a json response by using the Flask's app.response_class function and passing in three arguments:
    response = app.response_class(
        response = json.dumps({'text': text}),
        status = 200,
        mimetype= "application/json"
    )

    print(response)
    print(response.data)
    return response

@app.route('/process-message', methods=['POST'])
def process_message_route():
    return None


if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
