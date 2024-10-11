from django.http import HttpResponse


def item_list(request):
    return HttpResponse('<body>Список элементов</body>')


def item_detail(request, pk):
    return HttpResponse('<body>Подробно элемент</body>')


def re_item_detail(request, pk):
    return HttpResponse(f'<body>{pk}</body>')


def converter_item_detail(request, pk):
    return HttpResponse(f'<body>{pk}</body>')
