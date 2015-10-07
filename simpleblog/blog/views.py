from django.http import Http404
from django.shortcuts import render

from .models import Article


def index(request):
    articles = Article.objects.published()
    vars = {
        'objects': articles,
    }
    return render(request, 'index.html', vars)


def article(request, slug):
    try:
        article = Article.objects.filter(slug=slug).get()
    except Article.DoesNotExist:
        raise Http404('No Article matches the given query.')
    vars = {
        'object': article,
    }
    return render(request, 'article.html', vars)