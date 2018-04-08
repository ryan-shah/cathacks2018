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
    bad_text_tags = [line.rstrip('\n').lower() for line in open('text_tags.txt')]
    words = data['text'].split(' ')
    for word in words:
        if word.lower() in bad_text_tags:
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
    access_token = 'EAACEdEose0cBALOGZBqvEDOFaZB7I5ybALXExC7vODPdbnV1rjWu9AhCWIThdS08HfqycFGB2wt3r1awo7vZAxCtzvu8zyvDsHuVrAZCwM1iH7vq4nhL0Nv7cAkfFFyWUBzZAMcBsCRTkA9dTmLahUKs3NOIzH1bW7LyALrG09EjPSQd67TFrs1fgXGY26mwZBgSBCay2u82PF4fTISg811Cpky9BTkFEZD'

    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object('me')
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
                if check is not '':
                    item['msg'] = check
                    result.append(item)
            posts = requests.get(posts['paging']['next']).json()
        except KeyError:
            break
    return result

print(getPosts())
