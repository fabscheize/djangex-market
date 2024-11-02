import re

from django.conf import settings

__all__ = []


WORDS_REGEX = re.compile(r'\w+|\W+')
RUSSIAN_REGEX = re.compile(r'^[а-яА-яёЁ]+$')


def reverse_russian_words(string) -> str:
    words = re.findall(WORDS_REGEX, string)

    transformed_words = [
        word[::-1] if RUSSIAN_REGEX.search(word) else word for word in words
    ]

    return ''.join(transformed_words)


class ReverseMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def is_need_to_reverse(cls) -> bool:
        if not settings.ALLOW_REVERSE:
            return False

        cls.count = (cls.count + 1) % 10
        if cls.count % 10 != 0:
            return False
        cls.count = 0
        return True

    def __call__(self, request):
        response = self.get_response(request)

        if self.is_need_to_reverse():
            content = response.content.decode('utf-8')
            response.content = reverse_russian_words(content).encode('utf-8')

        return response
