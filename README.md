# Influencer GPT

Automatic content generator for Instagram. This code powers [@purrfectissimo](https://www.instagram.com/purrfectissimo/) instagram.

It uses ChatGPT API to generate Instagram posts ideas, DALLE2 to convert them into images. 

Google Cloud is used as a platform to run this code on schedule and host images.


## How to use it?
This repository contains a function code, intended to be run on Google Cloud Functions. `main.py` contains cloud functions code and `test.py` can be run locally.

You will need the following:

- Google Cloud account
- Cloud Storage Bucket with `igpt_public` name and fine-grained access enabled
- Instagram Business Account
- Instagram Access token and instagram account ID. You can use the following tutorials to get them:
  - Access Instagram API using https://superface.ai/blog/instagram-login
  - How to get Instagram API Token using Postman: https://www.youtube.com/watch?v=iN9Y7twSz7M&t=529
- Open AI API Key

Generator needs the following environment variables

- `OPENAI_API_KEY`  - Your Open AI API Key
- `IG_ACCOUNT_ID`   - Your Instagram Account ID
- `IG_ACCESS_TOKEN` - Your Instagram Access Token
- `GOOGLE_APPLICATION_CREDENTIALS` - **Local run only**. You need to set relative path to your GCP Service Account credentials. Service account should have write & object admin access to `igpt_public` bucket


## High level cloud application overview

- GCS(Google Cloud Storage) bucket `igpt_public` stores jpg images of your instagram content
- GCF(Google Cloud Functions) function has all the code from this repository
  - `generate_post` function used as an entry point for http-triggered cloud function
  - `generate_post_pubsub` used for Pub/Sub trigger 
- GCF function generates content using OpenAI APIs. GCS bucket is needed to store content files converted to JPG. Instagram API require them to be accessible on the internet.
- Full automation achieved by Pub/Sub topic which triggers GCF function and a Cloud Scheduler job which periodically publishes messages to this Pub/Sub topic.

The message content has the following format:

```
{
  "idea": "A picture of cat doing funny things.",
  "dry_run": false
}
```