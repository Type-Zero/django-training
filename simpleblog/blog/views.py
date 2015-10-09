from django.http import Http404
from django.shortcuts import render

from .models import Article, Tag


def index(request):
    articles = Article.objects.published().prefetch_related('tags')
    vars = {
        'objects': articles,
    }
    return render(request, 'index.html', vars)


def article(request, slug):
    try:
        article = Article.objects.filter(slug=slug).prefetch_related('tags').get()
    except Article.DoesNotExist:
        raise Http404('No Article matches the given query.')
    vars = {
        'object': article,
    }
    return render(request, 'article.html', vars)


def tag(request, tag_slug):
    try:
        tag = Tag.objects.filter(slug=tag_slug).get()
    except Tag.DoesNotExist:
        raise Http404('No Tag matches the given query.')
    
    articles = Article.objects.published().tagged_with_slug(tag_slug).values('slug', 'title', 'created')
    
    vars = {
        'tag': tag,
        'objects': articles,
    }
    return render(request, 'selection.html', vars)