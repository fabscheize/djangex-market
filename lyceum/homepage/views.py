from http import HTTPStatus

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.urls import reverse


import catalog.models
from homepage.forms import EchoForm

__all__ = []


def home(request):
    template = 'homepage/main.html'
    items = catalog.models.Item.objects.on_main()
    context = {'items': items}
    return render(request, template, context)


def coffee(request):
    return HttpResponse('Я чайник', status=HTTPStatus.IM_A_TEAPOT)


def echo(request):
    template = 'homepage/echo.html'
    echo_form = EchoForm(request.POST or None)
    context = {
        'echo_form': echo_form,
    }

    if request.method == 'POST':
        if echo_form.is_valid():
            text = echo_form.cleaned_data['text']
            request.session['submitted_text'] = text
            return redirect(reverse('homepage:submit'))

    for field in echo_form:
        if field.errors:
            field.field.widget.attrs['class'] = (
                field.field.widget.attrs.get('class', '') + ' is-invalid'
            )

    return render(request, template, context)


def submit(request):
    text = request.session.pop('submitted_text', None)
    if text is None:
        return HttpResponseNotAllowed(['POST'])

    return HttpResponse(text, content_type='text/plain; charset=utf-8')
