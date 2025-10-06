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
    user_message = request.json['userMessage'] # Get user's message from their request
    print('user_message', user_message)

    voice = request.json['voice'] # Get user\'s preferred voice from their request
    print('voice', voice)

    # Call watsonx_process_message function to process the user's message and get a response back
    watsonx_response_text = watsonx_process_message(user_message)

    # Clean the response to remove any emptylines
    watsonx_response_text = os.linesep.join([s for s in watsonx_response_text.splitlines() if s])

    # Call our text_to_speech function to convert Watsonx Api's reponse to speech
    watsonx_response_speech = text_to_speech(watsonx_response_text, voice)

    # convert watsonx_response_speech to base64 string so it can be sent back in the JSON response
    '''As the watsonx_response_speech is a type of audio data, we can't directly send this inside a json as it can only store textual data. Therefore, we will be using something called "base64 encoding". We can convert any type of binary data to a textual representation by encoding the data in base64 format. Hence, we will simply use base64.b64encode(watsonx_response_speech).decode('utf-8') and store the result back to watsonx_response_speech.
    '''
    watsonx_response_speech = base64.b64encode(watsonx_response_speech).decode('utf-8')

    # Send a JSON response back to the user containing their message\'s response both in text and speech formats
    '''
    Now we have everything ready for our response so finally we will be using the same app.response_class function and send in the three parameters required. The status and mimetype will be exactly the same as we defined them in our previous speech_to_text_route. In the response we will use json.dumps function as we did before and will pass in a dictionary as a parameter containing "watsonxResponseText":watsonx_response_text and "watsonxResponseSpeech":watsonx_response_speech.
    '''
    response = app.response_class(
        response=json.dumps({"watsonxResponseText": watsonx_response_text, "watsonxResponseSpeech": watsonx_response_speech}),
        status=200,
        mimetype='application/json'
    )
    print(response)
    return response


if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
