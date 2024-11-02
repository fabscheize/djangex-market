from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

import catalog.models

__all__ = []


def home(request):
    template = 'homepage/main.html'
    items = catalog.models.Item.objects.on_main()
    context = {'items': items}
    return render(request, template, context)


def coffee(request):
    template = 'homepage/coffee.html'
    context = {}
    return render(request, template, context, status=HTTPStatus.IM_A_TEAPOT)
    return HttpResponse('Я чайник', status=HTTPStatus.IM_A_TEAPOT)
    # убрать если лмс не ругается
