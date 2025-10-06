import os

# To call watsonx's LLM, we need to import the library of IBM Watson Machine Learning
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.foundation_models import Model

# placeholder for Watsonx_API and Project_id incase you need to use the code outside this environment
# API_KEY = "Your WatsonX API"
# PROJECT_ID= "skills-network"
PROJECT_ID = os.environ["WATSONX_PROJECT_ID"]  # Line / Own details added

# Define the credentials 
credentials = {
    # "url": "https://us-south.ml.cloud.ibm.com"
    os.getenv("IBM_WATSON_URL", "https://us-south.ml.cloud.ibm.com")   # Line / Own details added
    #"apikey": API_KEY
}
    
# Specify model_id that will be used for inferencing
model_id = "mistralai/mistral-medium-2505"


# Define the model parameters
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import DecodingMethods

parameters = {
    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
    GenParams.MIN_NEW_TOKENS: 1,
    GenParams.MAX_NEW_TOKENS: 1024
}

# Define the LLM
model = Model(
    model_id=model_id,
    params=parameters,
    credentials=credentials,
    project_id=PROJECT_ID
)


def watsonx_process_message(user_message):
    # Set the prompt for watsonx api - using a strict translation instruction
    prompt = prompt = f"""
    Translate the following English sentence into Spanish. 
    Reply ONLY with the translation, no explanations, no formatting, no extra text.
    English: {user_message}
    Spanish:
    """
    response_text = model.generate_text(prompt=prompt)
    print("Watsonx response: ", response_text)
    return response_text.strip()

###########

import requests

def speech_to_text(audio_binary):

    # Set up Watson Speech-to-Text HTTP Api url
    # Remember to replace the ... for the base_url variable with the URL for your Speech-to-Text model (for example,https://sn-watson-stt.labs.skills.network that is available for use in lab environment only)
    base_url = '...'
    api_url = base_url+'/speech-to-text/api/v1/recognize'

    # Set up parameters for our HTTP reqeust
    params = {
        'model': 'en-US_Multimedia',  # one key-value pair i.e. 'model': 'en-US_Multimedia' which tells Watson that we want to use the US English model for processing our speech
    }

    # Set up the body of our HTTP request - sending the audio data inside the body of our POST request
    body = audio_binary

    # Send a HTTP Post request
    response = requests.post(api_url, params=params, data=audio_binary).json()
    '''using the requests library to send this HTTP request passing in the URL, params, and data(body) to it and then use .json() to convert the API's response to json format which is very easy to parse and can be treated like a dictionary in Python.
    The structure of the response is something like this:
    {
        "response": {
            "results": {
            "alternatives": {
                "transcript": "Recognised text from your speech"
            }
            }
        }
    }
    
    '''

    # Parse the response to get our transcribed text
    text = 'null'
    while bool(response.get('results')):
        print('Speech-to-Text response:', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognised text: ', text)
        return text
    
###########

def text_to_speech(text, voice=""):
    return None
