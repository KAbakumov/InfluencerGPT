"""Functions to post content to Facebook using Facebook API"""
import os
import requests
import urllib.parse

IG_ACCOUNT_ID = os.getenv("IG_ACCOUNT_ID")
IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")

IG_HEADERS = {"Authorization": f"Bearer {IG_ACCESS_TOKEN}"}

def escape(text: str) -> str:
    """Escapes text for use in Instagram API query params"""
    return urllib.parse.quote(text, safe="") 

def instagramCreateMediaContent(caption: str, image_url: str) -> str:
    """Posts an image to Instagram"""
    #url encode caption parameter    
    response = requests.post(f"https://graph.facebook.com/{IG_ACCOUNT_ID}/media?caption={escape(caption)}&image_url={escape(image_url)}",
                             headers=IG_HEADERS)
    if (response.status_code != 200):
        raise Exception(
            f"HTTP Error: {response.status_code} '{response.text}'")
    else:
        return response.json()["id"]


def postToInstagram(caption: str, image_url: str):
    """Posts an image to Instagram"""
    media_id = instagramCreateMediaContent(caption, image_url)
    response = requests.post(f"https://graph.facebook.com/{IG_ACCOUNT_ID}/media_publish?creation_id={media_id}",
                             headers=IG_HEADERS)
    if (response.status_code != 200):
        raise Exception(
            f"HTTP Error: {response.status_code} '{response.text}'")
    else:
        return response.json()["id"]
