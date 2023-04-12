"""Module which converts images to jpg and uploads to Cloud Storage"""
import requests
import uuid

from google.cloud import storage
from io import BytesIO
from PIL import Image

def convertToJpg(url: str):
    """Downloads image from url and converts to jpg"""
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    # get img content in memory as jpeg bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    return img_bytes

def writeImageToFile(filename: str, img_bytes: BytesIO):
    # write img_bytes to file
    with open(filename, 'wb') as f:
        f.write(img_bytes.getvalue())


def writeImageToGCS(img_bytes: BytesIO, bucket_name: str, filename: str):
    """Uploads image to Google Cloud Storage"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_string(img_bytes.getvalue(), content_type='image/jpeg')
    #allow public access to this blob
    blob.make_public()
    return blob.public_url

BUCKET_NAME = "igpt_public"
def convertAndWriteToBucket(url: str):
    """Downloads image from url, converts to jpg, and uploads to GCS bucket"""
    img_bytes = convertToJpg(url)
    filename = str(uuid.uuid4()) + ".jpg"
    return writeImageToGCS(img_bytes, BUCKET_NAME, filename)
    