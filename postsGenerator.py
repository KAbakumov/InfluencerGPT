import json
import os
import re
import requests

from types import SimpleNamespace

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

POST_IDEA_PROMPT="""
 Give me an idea of a picture where cat doing things which humans usually do,
 describe the color and breed of the cat and what it is doing.
 Please don't include laptop or glasses
"""

POST_DESCRIPTION_PROMPT="""
Generate a description for the Instagram Post from the following \
    description of the photo: '%s' Include instagram tags. \
    Output only the description text.
"""

CHAT_GPT_HEADERS = {"Content-Type": "application/json",
               "Authorization": f"Bearer {OPENAI_API_KEY}"}
def chatGptComplete(prompt: str, max_tokens: int) -> str:
    """ Rest call to ChatGPT API to return a short and consistent answer on a prompt."""
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 1.5,
        "max_tokens": max_tokens
    }
    
     
    response = requests.post("https://api.openai.com/v1/chat/completions",
                             json=data, headers=CHAT_GPT_HEADERS)
    if(response.status_code != 200):
        raise "HTTP Error: " + response.status_code
    else:
        json_data = response.text
        resp = json.loads(
            json_data, object_hook=lambda d: SimpleNamespace(**d))
        return resp.choices[0].message.content

def chatGptGenerateImage(prompt: str) -> str:
   """Generates an image from promt and returns the image URL"""
   data = {
     "prompt": prompt,
     "n": 1,
     "size": "1024x1024"
   }
   response = requests.post("https://api.openai.com/v1/images/generations",
          json=data, headers=CHAT_GPT_HEADERS)
   if(response.status_code != 200):
        raise Exception(f"HTTP Error: {response.status_code} '{response.text}'")  
   else:
        json_data = response.text
        resp = json.loads(
            json_data, object_hook=lambda d: SimpleNamespace(**d))
        return resp.data[0].url


def generatePostIdea() -> str: 
  return chatGptComplete(POST_IDEA_PROMPT, 100)

def generatePostDescription(idea: str):
    return chatGptComplete(POST_DESCRIPTION_PROMPT % idea, 200)


idea = generatePostIdea()
print(f"Post idea: '{idea}'\n")
pictureUrl = chatGptGenerateImage(idea)
description = generatePostDescription(idea)

print(pictureUrl)
print(description)

# Access Instagram API using https://superface.ai/blog/instagram-login
# How to get Instagram API Token using Postman: https://www.youtube.com/watch?v=iN9Y7twSz7M&t=529 