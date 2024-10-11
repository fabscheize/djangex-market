import re

from django.conf import settings


def reverse_russian_words(string):
    delimiters = [
        ' ',
        '.',
        ',',
        '!',
        '?',
        '(',
        ')',
        ';',
        ':',
        '"',
        '-',
        "'",
        '<',
        '>',
        '/',
    ]
    regex_pattern = '|'.join(map(re.escape, delimiters))
    all_words = re.split(regex_pattern, string)
    all_words = [word for word in all_words if word != '']

    for word in all_words:
        if re.fullmatch(r'[А-Яа-яёЁ]+', word) is not None:
            string = string.replace(word, word[::-1])

    return string


class ReverseMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.ALLOW_REVERSE:
            ReverseMiddleware.count += 1

            if ReverseMiddleware.count == 10:
                ReverseMiddleware.count = 0
                content = response.content.decode('utf-8')
                reversed_content = reverse_russian_words(content)
                response.content = reversed_content.encode('utf-8')

        return response
