from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse(render(request, 'app/index.html'))


def results(request):
    # What needs to happen here?
    #   - Data from the given website request (Facebook or Twitter) needs to be pulled, processed
    #   - Data needs to be organized in a meaningful way: images vs text, severity
    pass
