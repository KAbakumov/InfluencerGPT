import posts_generator
import os

def testPostGenerator():
    post = posts_generator.generatePost()
    print(post.pictureUrl)
    print(post.description)


def testInstagramPoster():
    #Set environment variable to point to the credentials file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
    post = posts_generator.generatePostAndPublish("an oil painting of a cat doing funny things. Please include cat breed and color. Describe in one short sentence")
    


posts_generator.generatePost("Cats doing funny things. Please include cat breed and color. Describe in a single short sentence.")
# Access Instagram API using https://superface.ai/blog/instagram-login
# How to get Instagram API Token using Postman: https://www.youtube.com/watch?v=iN9Y7twSz7M&t=529
