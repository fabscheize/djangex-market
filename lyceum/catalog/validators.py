import re

from django.core import exceptions
from django.utils import deconstruct


@deconstruct.deconstructible
class ValidateContainsWords(object):
    def __init__(self, *words):
        self.words = words
        self.pattern = re.compile(
            r'\b(' + '|'.join(re.escape(word) for word in words) + r')\b',
            re.IGNORECASE,
        )

    def __call__(self, text):
        if not self.pattern.search(text):
            raise exceptions.ValidationError(
                (
                    'Убедитесь, что в тексте есть одно из следующих слов: '
                    f'{", ".join(self.words)}'
                ),
                params={'text': text},
            )
