from http import HTTPStatus
import json

from django.http import HttpResponse
from django.shortcuts import render

from lyceum import settings

__all__ = []

ITEMS_FILE_PATH = settings.BASE_DIR / 'static_dev/files/items.json'


def load_items():
    with open(ITEMS_FILE_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)


def home(request):
    template = 'homepage/main.html'
    items = load_items()
    context = {'items': items}
    return render(request, template, context)


def coffee(request):
    return HttpResponse('Я чайник', status=HTTPStatus.IM_A_TEAPOT)
