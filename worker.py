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


def speech_to_text(audio_binary):
    return None

def text_to_speech(text, voice=""):
    return None

def watsonx_process_message(user_message):
    # Set the prompt for watsonx api - using a strict translation instruction
    prompt = """Respond to the user query: '''{user message}'''"""
    response_text = model.generate_text(prompt=prompt)
    print("Watsonx response: ", response_text)
    return response_text.strip()
