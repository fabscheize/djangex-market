from http import HTTPStatus

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render


import catalog.models
from homepage.forms import EchoForm

__all__ = []


def profile(request):
    template = 'homepage/main.html'
    items = catalog.models.Item.objects.on_main()
    context = {'items': items}
    return render(request, template, context)


def user_list(request):
    profile = request.user.profile
    profile.coffee_count += 1
    profile.save()

    template = 'homepage/coffee.html'

    return render(request, template, status=HTTPStatus.IM_A_TEAPOT)
    return HttpResponse('Я чайник', status=HTTPStatus.IM_A_TEAPOT)


def user_detail(request):
    profile = request.user.profile
    profile.coffee_count += 1
    profile.save()

    template = 'homepage/coffee.html'

    return render(request, template, status=HTTPStatus.IM_A_TEAPOT)
    return HttpResponse('Я чайник', status=HTTPStatus.IM_A_TEAPOT)
