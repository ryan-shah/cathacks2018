"""
A simple example script to get all posts on a user's timeline.
Originally created by Mitchell Stewart.
<https://gist.github.com/mylsb/10294040>
"""
import facebook
import requests
from app import image_processing


def format_post(data):
    """ Here you might want to do something with each post. E.g. grab the
    post's message (post['message']) or the post's picture (post['picture']).
    In this implementation we just print the post's created time.
    """
    result = {"img": "", 'text': '', 'link': '', 'msg': '', 'date': ''}
    try:
        result['text'] = data['message']
    except:
        pass
    try:
        result['img'] = data['full_picture']
    except:
        pass
    result['date'] = data['created_time']
    result['link'] = data['permalink_url']
    return result


def analyzePost(data):
    bad_text_tags = [line.rstrip('\n') for line in open(r"C:\Users\alija\Downloads\text_tags.txt")]
    words = data['text'].split(' ')
    for word in words:
        if word in bad_text_tags:
            return "Post contains inappropriate word, '" + word + "'"
    try:
        image_data = image_processing.analyzeImage(data['img'])
    except:
        return ''
    image_results = image_processing.checkImageData(image_data)
    if image_results is not '':
        return image_results
    return ''


def getPosts():
    # You'll need an access token here to do anything.  You can get a temporary one
    # here: https://developers.facebook.com/tools/explorer/
    access_token = 'EAACEdEose0cBACUR85suq9pZCfr8l1JaRSDE3TEFQFiWic8nItTrXEeCZAUpC1ZBxRnqN4EUDcv556i4YDUWJpKR7BfAdG9aYqvbU3rjNIbbExTEQqZBztvjHRgQbTtqXyiTvURcKKzRz4TnuCJQV5XBfMONh08rIr8m7ry8hdDZAHNZCWsZCZB4qh4IByG2hbODwNZABwLoZANtih5UCQ6Um9ocQGZAql6V5cZD'

    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object('me')
    posts = graph.get_connections(id='me', connection_name='posts',
                                  fields="message,full_picture,created_time,permalink_url")
    # Wrap this block in a while loop so we can keep paginating requests until
    # finished.
    # Perform some action on each post in the collection we receive from
    # Facebook.
    result = []
    while True:
        try:
            for post in posts['data']:
                item = format_post(post)
                check = analyzePost(item)
                if check is not '':
                    item['msg'] = check
                    result.append(item)
            posts = requests.get(posts['paging']['next']).json()
        except KeyError:
            break
    return result
