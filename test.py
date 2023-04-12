import posts_generator
import os

def testInstagramPoster():
    post = posts_generator.generatePostAndPublish("an oil painting of a cat doing funny things. Please include cat breed and color. Describe in one short sentence")

def testPostsGenerator():
    posts_generator.generatePost("Cats doing funny things. Please include cat breed and color. Describe in a single short sentence.")


testPostsGenerator()

# Uncomment to test Instagram Posting
# testInstagramPoster()