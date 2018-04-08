from django.http import HttpResponse
from django.shortcuts import render

from app import facebook_posts


def index(request):
    return HttpResponse(render(request, 'app/index.html'))


def render_load(request):
    return HttpResponse(render(request, 'app/loading.html'))


def load_data(request):
    posts_with_information = facebook_posts.getPosts()
    data = {'posts': posts_with_information}
    return HttpResponse(render(request, 'app/results.html', data))


def results(request):
    # What needs to happen here?
    #   - Data from the given website request (Facebook or Twitter) needs to be pulled, processed
    #   - Data needs to be organized in a meaningful way: images vs text, severity
    posts_with_information = [
        {
            'img': '',  # Link to the image source
            'text': 'This is a post that is not very long',
            'link': 'blah',  # Link to the actual post
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
            'img': r"https://cdn.cnn.com/cnnnext/dam/assets/161017153320-dea-schedule-1-drugs-heroin-exlarge-169.jpg",
            'text': 'Man this is so lit',
            'link': 'something',
            'msg': 'This image was flagged for: drugs',
            'date': 'someday'
        },
        {
            'img': '',
            'text': 'Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.',
            'link': 'something',
            'msg': 'This is long',
            'date': 'someday'
        }
    ]

    posts_with_information = facebook_posts.getPosts()

    data = {'posts': posts_with_information}
    return HttpResponse(render(request, 'app/results.html', data))
