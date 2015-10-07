[← Previous](3-Application.md) | [Index](README.md) | Next →

# Views and Templates

## Simple View

```python
# blog/views.py
from django.shortcuts import render

from .models import Article

def index(request):
    articles = Article.objects.published()
    vars = {
        'objects': articles,
    }
    return render(request, 'index.html', vars)
```

## Associated Template

Creation of the associated template, _index.html_ under a new _templates/_ folder inside _blog/_:

```html
<!-- blog/templates/index.html -->
{% for object in objects %}
<div>
    <h1>{{ object.title }}</h1>
    <p>{{ object.body }}</p>
    <em>Created: {{ object.created }}{% if object.updated %} | Last edited: {{ object.updated }}{% endif %}</em>
</div>
{% endfor %}
```

## Routing System

Have the project's urls include the 'blog' _urls.py_ module:

```python
# simpleblog/urls.py
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('blog.urls')),
]
```  

Creation of a _urls.py_ inside _blog/_

```python
# blog/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
```

## Details View and Templates

Creation of view, template and URL for detailed Article pages:

```python
# blog/views.py
...
def article(request, slug):
    try:
        article = Article.objects.filter(slug=slug).get()
    except Article.DoesNotExist:
        raise Http404('No Article matches the given query.')
    vars = {
        'object': article,
    }
    return render(request, 'article.html', vars)
```
```html
<!-- blog/templates/article.html -->
<a href="{% url 'index' %}">← Back</a>
<div>
    <h1>{{ object.title }}</h1>
    <p>{{ object.body }}</p>
    <em>Created: {{ object.created }}{% if object.updated %} | Last edited: {{ object.updated }}{% endif %}</em>
</div>
```

```python
# blog/urls.py
...
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^articles/(?P<slug>\S+)$', views.article, name='details'),
]
```

```html
<!-- blog/templates/index.html -->
...
    <h1><a href="{% url 'details' object.slug %}">{{ object.title }}</a></h1>
    <p>{{ object.body }}</p>
...
```