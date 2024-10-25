import json

# from django.http import HttpResponse
from django.shortcuts import render

from lyceum import settings

ITEMS_FILE_PATH = settings.BASE_DIR / 'static_dev/files/items.json'


def load_items():
    """Функция для загрузки данных из JSON файла"""
    with open(ITEMS_FILE_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)


def item_list(request):
    template = 'catalog/item_list.html'
    items = load_items()
    context = {'items': items}
    return render(request, template, context)


def item_detail(request, pk):
    template = 'catalog/item.html'
    items = load_items()
    item = next((item for item in items if item['pk'] == pk), None)

    if item is None:
        return render(
            request,
            '404.html',
        )

    context = {'item': item}
    return render(request, template, context)
