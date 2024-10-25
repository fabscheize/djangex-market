import json

from django.http import Http404, HttpResponse
from django.shortcuts import render

from lyceum import settings

__all__ = []

ITEMS_FILE_PATH = settings.BASE_DIR / 'static_dev/files/items.json'


def load_items():
    with open(ITEMS_FILE_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)


def item_list(request):
    template = 'catalog/item_list.html'
    items = load_items()
    context = {'items': items}
    return render(request, template, context)


def item_detail(request, pk):
    if int(pk) > 5:
        return HttpResponse(f'<body>{pk}</body>')

    template = 'catalog/item.html'
    items = load_items()
    item = next((item for item in items if item['pk'] == int(pk)), None)

    if item is None:
        raise Http404('Товар не найден')

    context = {'item': item}
    return render(request, template, context)
