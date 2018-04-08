"""
A simple example script to get all posts on a user's timeline.
Originally created by Mitchell Stewart.
<https://gist.github.com/mylsb/10294040>
"""
import facebook
import requests
import json

def some_action(post):
    """ Here you might want to do something with each post. E.g. grab the
    post's message (post['message']) or the post's picture (post['picture']).
    In this implementation we just print the post's created time.
    """
    print('id:',post['id'])
    print('message',post['message'])
    print('image',post['full_picture'])
    print('time',post['created_time'])
    print('url',post['permalink_url'])
    print()


# You'll need an access token here to do anything.  You can get a temporary one
# here: https://developers.facebook.com/tools/explorer/
access_token = 'EAACEdEose0cBAIcOZCOIvcyZBgGWjqZAC0PPqAGQTv5ZB7aqb05tPhKG0MRXZCLeKZAUerbHUGz661hDrsRguY3R9zqAax7QFuZAiXcwejxKT15ZB22TQvkEKfYCT2N1RYykuQlDsvRSoPSdmoWEf09EQ83ViyjPYpNHoHdFI9ci3PKysNE1qDSCSAFdVYP4kElLPyQxnESXEUOdZCTWZC8lURzLhd5vIPZCYkZD'
# Look at Bill Gates's profile for this example by using his Facebook id.
user = '110355093151719'

graph = facebook.GraphAPI(access_token)
profile = graph.get_object(user)
posts = graph.get_connections(id='me', connection_name='posts', fields="id,message,full_picture,created_time,permalink_url")
# Wrap this block in a while loop so we can keep paginating requests until
# finished.
count = 0
while True:
    try:
        # Perform some action on each post in the collection we receive from
        # Facebook.
        print(json.dump(posts))
        [some_action(post=post) for post in posts['data']]
        # Attempt to make a request to the next page of data, if it exists.
        posts = requests.get(posts['paging']['next']).json()
    except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
        break
print(count)
