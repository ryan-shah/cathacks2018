from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse(render(request, 'app/index.html'))


def results(request):
    # What needs to happen here?
    #   - Data from the given website request (Facebook or Twitter) needs to be pulled, processed
    #   - Data needs to be organized in a meaningful way: images vs text, severity
    posts_with_information = [
        {
            'img': '',  # Link to the image source
            'text': 'This is a post that is not very long',
            'link': 'blah', # Link to the actual post
            'msg': 'violence',
            'date': 'Someday'
        },
        {
            'img': '',
            'text': 'This post is just a little bit longer than the last one, but still not too bad',
            'link': 'something',
            'msg': 'vulgarity',
            'date': 'someday'
        },
        {
            'img': '',
            'text': 'Another post with text',
            'link': 'something',
            'msg': 'drugs',
            'date': 'someday'
        },
        {
            'img': '',
            'text': 'Wow another post with another box of text',
            'link': 'something',
            'msg': 'badness',
            'date': 'someday'
        }
    ]
    data = {'posts': posts_with_information}
    return HttpResponse(render(request, 'app/results.html', data))
