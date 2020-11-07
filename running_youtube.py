import json
import os
import sys
import requests
import time

import json
import tensorflow.compat.v1 as tf
import tensorflow_hub as hub
import numpy as np

import os
from sklearn.metrics.pairwise import cosine_similarity,cosine_distances
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO

graph = tf.Graph()
print("Downloading pre-trained embeddings from tensorflow hub...")
tf.disable_eager_execution()
embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/2")
text_ph = tf.placeholder(tf.string)
embeddings = embed(text_ph)
print("Done.")

print("Creating tensorflow session...")
session = tf.Session()
session.run(tf.global_variables_initializer())
session.run(tf.tables_initializer())
print("Done.")


questionAnswerList = {"What is operating system?": "An operating system (OS) is system software that manages computer hardware, software resources, and provides common services for computer programs. Time-sharing operating systems schedule tasks for efficient use of the system and may also include accounting software for cost allocation of processor time, mass storage, printing, and other resources.", "Study Test": "I will study and work hard."}



def createTensorflowSession():
    graph = tf.Graph()
    print("Downloading pre-trained embeddings from tensorflow hub...")
    tf.disable_eager_execution()
    embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/2")
    text_ph = tf.placeholder(tf.string)
    embeddings = embed(text_ph)
    print("Done.")

    print("Creating tensorflow session...")
    session = tf.Session()
    session.run(tf.global_variables_initializer())
    session.run(tf.tables_initializer())
    print("Done.")

def ocrComputation(image_url):
    missing_env = False
    os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY'] = '51b659e757ca4a0f8422f46559fa827b'
    os.environ['COMPUTER_VISION_ENDPOINT'] = 'https://southcentralus.api.cognitive.microsoft.com/'
    # Add your Computer Vision subscription key and endpoint to your environment variables.
    if 'COMPUTER_VISION_ENDPOINT' in os.environ:
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
    else:
        print("From Azure Cognitive Service, retrieve your endpoint and subscription key.")
        print("\nSet the COMPUTER_VISION_ENDPOINT environment variable, such as \"https://westus2.api.cognitive.microsoft.com\".\n")
        missing_env = True

    if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
    else:
        print("From Azure Cognitive Service, retrieve your endpoint and subscription key.")
        print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable, such as \"1234567890abcdef1234567890abcdef\".\n")
        missing_env = True

    if missing_env:
        print("**Restart your shell or IDE for changes to take effect.**")
        sys.exit()

    text_recognition_url = endpoint + "/vision/v3.1/read/analyze"

    # Set image_url to the URL of an image that you want to recognize.
    image_url = "https://raw.githubusercontent.com/adityaaggarwal19/Data-Mining/master/operating_system_answer.jpeg"
    #image_url = "https://raw.githubusercontent.com/pranavgurditta/Demo-Custom-Vision-AI/master/demo-ocr-check-image.jpeg?token=AD3T6BUNRY5KBOM4YSPJDRS7T7HPM"

    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    data = {'url': image_url}
    response = requests.post(text_recognition_url, headers = headers, json = data)
    response.raise_for_status()

    # Extracting text requires two API calls: One call to submit the
    # image for processing, the other to retrieve the text found in the image.

    # Holds the URI used to retrieve the recognized text.
    operation_url = response.headers["Operation-Location"]

    # The recognized text isn't immediately available, so poll to wait for completion.
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        
        #print(json.dumps(analysis, indent=4))

        time.sleep(1)
        if ("analyzeResult" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'failed'):
            poll = False

    polygons = []
    if ("analyzeResult" in analysis):
        # Extract the recognized text, with bounding boxes.
        polygons = [(line["boundingBox"], line["text"])
                    for line in analysis["analyzeResult"]["readResults"][0]["lines"]]
        answer_text = ""
    
        for i in range(0, len(analysis["analyzeResult"]["readResults"][0]["lines"])):
            answer_text = answer_text + " " + analysis["analyzeResult"]["readResults"][0]["lines"][i]["text"]
    
    return answer_text

def embed_text(text):
    vectors = session.run(embeddings, feed_dict={text_ph: text})
    return [vector.tolist() for vector in vectors]

def getCandidateAnswerScore(question,answer_text):
    #candidateAnswer = input("Enter candidate answer: ")
    #candidateAnswerVector = embed_text([candidateAnswer])[0]
    print("ques",question)
    print("candidate ans",answer_text)
    print("actual ans",questionAnswerList[question])
    candidateAnswerVector = embed_text([answer_text])[0]
  
    #correctAnswerVector = embed_text([questionAnswerList["What is operating system?"]])[0]
    correctAnswerVector = embed_text([questionAnswerList[question]])[0]
   
    candidateAnswerVecto = []
    candidateAnswerVecto.append(candidateAnswerVector)
    correctAnswerVecto = []
    correctAnswerVecto.append(correctAnswerVector)
    cos_sim = cosine_similarity(candidateAnswerVecto, correctAnswerVecto, dense_output=True)
    print (f"Cosine Similarity between A and B:{cos_sim}")
    print (f"Cosine Distance between A and B:{1-cos_sim}")

def computeSimilarity(question, answer, documentURL):
  
    #createTensorflowSession()
    answer_text = ocrComputation(documentURL)
    #gettingQuestionAnswers()

    getCandidateAnswerScore(question,answer)
    '''
    print("Closing tensorflow session...")
    session.close()
    print("Done.")
    '''

