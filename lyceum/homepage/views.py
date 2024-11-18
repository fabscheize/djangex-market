from http import HTTPStatus

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render


import catalog.models
from homepage.forms import EchoForm
import users.models

__all__ = []


def home(request):
    template = 'homepage/main.html'
    items = catalog.models.Item.objects.on_main()
    context = {'items': items}
    return render(request, template, context)


def coffee(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            profile.coffee_count += 1
            profile.save()
        except users.models.Profile.DoesNotExist:
            pass

    template = 'homepage/coffee.html'

    return HttpResponse('Я чайник', status=HTTPStatus.IM_A_TEAPOT)
    return render(request, template, status=HTTPStatus.IM_A_TEAPOT)


def echo(request):
    if request.method == 'POST':
        return HttpResponseNotAllowed(['GET'])

    template = 'homepage/echo.html'
    echo_form = EchoForm()
    context = {
        'echo_form': echo_form,
    }
    return render(request, template, context)


def submit(request):
    echo_form = EchoForm(request.POST)
    if request.method == 'POST' and echo_form.is_valid():
        text = echo_form.cleaned_data['text']
        return HttpResponse(
            text,
            content_type='text/plain; charset=utf-8',
        )

    return HttpResponseNotAllowed(['POST'])
