from django import template
import re

register = template.Library()

@register.filter
def replace(value, arg):
    """Заменяет подстроку в значении. Ожидает аргумент в формате 'old|new'."""
    old, new = arg.split('|')
    return value.replace(old, new)

@register.simple_tag
def test_tag():
    return "Test tag works!"

@register.filter
def youtube_embed_url(url):
    """
    Converts a YouTube URL to an embeddable URL.
    Example: 'https://www.youtube.com/watch?v=VIDEO_ID' -> 'https://www.youtube.com/embed/VIDEO_ID'
    """
    if not url:
        return url
    match = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)', url)
    return f'https://www.youtube.com/embed/{match.group(1)}?rel=0' if match else url

@register.filter
def strip_media_prefix(value):
    """
    Removes redundant '/media/' prefix from the image URL, ensuring only one '/media/' remains.
    Example: '/media/media/task_images/file.png' -> '/media/task_images/file.png'
    """
    if not value:
        return value
    return re.sub(r'^/media/(media/)?', '/media/', value)

@register.filter
def div(value, arg):
    """
    Divides value by arg and returns the result as a float.
    Handles division by zero and invalid inputs by returning 0.
    Example: {{ 10|div:2 }} -> 5.0
    """
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError, TypeError):
        return 0

@register.filter
def mul(value, arg):
    """
    Умножает value на arg и возвращает результат как float.
    Обрабатывает ошибки, возвращая 0 при некорректных входных данных.
    Пример: {{ 0.5|mul:100 }} -> 50.0
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0