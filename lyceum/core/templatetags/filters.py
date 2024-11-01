from django import template

__all__ = []

register = template.Library()


@register.filter
def truncate_words(value, num_words=10):
    words = value.split()[:num_words]
    return (
        ' '.join(words) + '...' if len(words) == num_words else ' '.join(words)
    )
