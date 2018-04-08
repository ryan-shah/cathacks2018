"""
A simple example script to get all posts on a user's timeline.
Originally created by Mitchell Stewart.
<https://gist.github.com/mylsb/10294040>
"""
import facebook
import requests
import image_processing

def format_post(data):
    """ Here you might want to do something with each post. E.g. grab the
    post's message (post['message']) or the post's picture (post['picture']).
    In this implementation we just print the post's created time.
    """
    result = {"img":"", 'text':'', 'link':'', 'msg':'', 'date':''}
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
    bad_text_tags = [line.rstrip('\n') for line in open('text_tags.txt')]
    words = data['text'.]split(' ')
    for word in words:
        if word in bad_text_tags:
            return "Post contains inappropriate word, '" + word + "'"
    try:
        image_data = image_processing.analyzeImage(data['img'])
        image_results = image_processing.cheeckImageData(image_data)
        if image_results not == '':
            return image_results
    except:
        pass

    return ''

def getPosts():
    # You'll need an access token here to do anything.  You can get a temporary one
    # here: https://developers.facebook.com/tools/explorer/
    access_token = 'EAACEdEose0cBANRGv9koQlZAxDcvqL10iIkYfJVVZAQIpYvN2fKmzZBrJiXCYnXQD7GzzQrtw9PEdIoUvWWR58WqxrmgMhFZASUvZBxh0ruh2DkbAbsBPJnjewnnOyJSjAQAwq4XOFkt76LjkGsxIZA5KWAPrPxzzo4rmZAavGPlUUU3DZCxvYEPHBiFu3sjZBZB9mGWi9XAuQopW88kSa32ZA9oatA9IgWV4YZD'

    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object(user)
    posts = graph.get_connections(id='me', connection_name='posts', fields="message,full_picture,created_time,permalink_url")
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
                if check not == '':
                    item['msg'] = check
                    result.append(item)
            posts = requests.get(posts['paging']['next']).json()
        except KeyError:
            break

print(getPosts())
