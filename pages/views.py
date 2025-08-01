from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def HomePage(request):
    template = loader.get_template('pages/home.html')
    context = {}
    return HttpResponse(template.render(context, request))


def About(request):
    context={}
    return render(request, 'pages/about.html', context)
