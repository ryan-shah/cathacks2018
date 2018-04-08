"""
A simple example script to get all posts on a user's timeline.
Originally created by Mitchell Stewart.
<https://gist.github.com/mylsb/10294040>
"""
import facebook
import requests

def some_action(post):
    """ Here you might want to do something with each post. E.g. grab the
    post's message (post['message']) or the post's picture (post['picture']).
    In this implementation we just print the post's created time.
    """
    print(post['picture'])


# You'll need an access token here to do anything.  You can get a temporary one
# here: https://developers.facebook.com/tools/explorer/
access_token = 'EAACEdEose0cBAIgln1th4kozhKmbbZAG0jpQNeoHzWgVxaoxCDfSAQ1tNS5UZARabbHwEl279JsGcy5QylgLoJLVZCXkZBgRiNB3dl6SMnnZA2d707D6ZAmCQV995BNl1HSQCZBvAx8VGmmbFGeuPhRCKCUdcWLUjpZC4YnD7oxlqbNacYXpj7Yr3CE2qk5MqPf9eNOPgmBmtQVZC9bDaC3stFU8hnPMpp5MZD'
# Look at Bill Gates's profile for this example by using his Facebook id.
user = '110355093151719'

graph = facebook.GraphAPI(access_token)
profile = graph.get_object(user)
posts = graph.get_connections(profile['id'], 'posts')

# Wrap this block in a while loop so we can keep paginating requests until
# finished.
count = 0
while True:
    try:
        # Perform some action on each post in the collection we receive from
        # Facebook.
        [some_action(post=post) for post in posts['data']]
        # Attempt to make a request to the next page of data, if it exists.
        posts = requests.get(posts['paging']['next']).json()
    except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
        break
print(count)
