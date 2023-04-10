import base64
import json
import posts_generator
import functions_framework

@functions_framework.http
def generate_post(request):
    """
    Cloud function code for HTTP trigger
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'idea' in request_json:
        idea = request_json['idea']
    elif request_args and 'idea' in request_args:
        idea = request_args['idea']
    else:
        idea = 'Cats'

    return posts_generator.generatePostAndPublish(idea)

@functions_framework.cloud_event
def generate_post_pubsub(cloud_event):
    """Cloud function code for pubsub trigger
    """   
    parsed_data = base64.b64decode(cloud_event.data["message"]["data"]) 
    print(f"Received pub/sub message: {parsed_data}")
    #Convert parsed data to json
    event = json.loads(parsed_data)
    idea = event['idea']
    dry_run = event['dry_run']

    if dry_run != False:
        posts_generator.generatePostAndPublish(idea)
    else:
        posts_generator.generatePost(idea)

