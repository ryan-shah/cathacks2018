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
    print(post['message'])


# You'll need an access token here to do anything.  You can get a temporary one
# here: https://developers.facebook.com/tools/explorer/
access_token = 'EAACEdEose0cBAMZB4ZBOFZCp99YY1I6whNJMlvwZBsZCKpoOt1T29nNMznY5Sz4f72y6dkUMPHBImH553q1urUa5di8DZABnRVWqKZBhVr22ZCyZChVXddJaGtKoLap3E3MUZBKoV7J32oNe2RuFZArLWg6fPv7elghfGNB1WzyPCqYpETOCSsUzy4ZAr1JjgB2SSctAPiFyaEp7DW3ZArPfwXrEYrK8EZCAot4uAZD'
# Look at Bill Gates's profile for this example by using his Facebook id.
user = '110355093151719'

graph = facebook.GraphAPI(access_token)
profile = graph.get_object(user)
posts = graph.get_connections(profile['id'], 'posts', fields="message,full_picture,created_time,permalink_url")

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
