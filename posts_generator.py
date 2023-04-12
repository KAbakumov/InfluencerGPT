import image_converter
import instagram_poster
import json
import os
import requests

from types import SimpleNamespace

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

POST_IDEA_PROMPT="""
 Give me an idea of %s
"""

DEFAULT_IDEA = """\
 a picture where cat doing things which humans usually do,\
 describe the color and breed of the cat and what it is doing.\
 Please don't include laptop or glasses. Describe in a short sentence.
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


def generatePostIdea(idea: str = DEFAULT_IDEA) -> str: 
  return chatGptComplete(POST_IDEA_PROMPT % (idea), 100)

def generatePostDescription(idea: str):
    return chatGptComplete(POST_DESCRIPTION_PROMPT % idea, 200)

def generatePost(idea_prompt: str = DEFAULT_IDEA):
    """Generates a post idea, image and description"""
    print("Generating instagram post...")
    idea = generatePostIdea(idea_prompt)
    print(f"\nPost Idea: {idea}")
    pictureUrl = chatGptGenerateImage(idea)    
    description = generatePostDescription(idea)
    print(f"\nGenerated post media:\nPictureUrl:{pictureUrl}\n\nDescription:{description}")
    return SimpleNamespace(pictureUrl=pictureUrl, description=description)
    
def generatePostAndPublish(idea_prompt: str):
    post = generatePost(idea_prompt)
    print("Converting and uploading to the Cloud Storage...")
    jpeg_url=image_converter.convertAndWriteToBucket(post.pictureUrl)
    print(f"Conversion done, picture URL: {jpeg_url}")
    ig_content_id=instagram_poster.postToInstagram(post.description, jpeg_url)
    print(f"Instagram post created, content ID: {ig_content_id}")
    return f"Success! contentId:{ig_content_id}"