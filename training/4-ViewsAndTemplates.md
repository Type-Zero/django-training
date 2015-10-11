[← Previous](training/3-Application.md) | [Index](README.md) | [Next →](training/5-StylingTemplates.md)

# Views and Templates

This chapter will present the Django **views** and **templates** systems, as well as the routing modules (**urls**) that link the views to the client navigation.

## Simple View

**Views** in Django are the components that collect, compute and format resources to prepare an HTTP _Response_ object in response to a client _Request_.

We will start with a simple _index_ view that will be responsible for gathering all the 'published' Articles to display to the client.

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

This view needs to render a **template**, an HTML-based frame to which data can be passed to format a final HTML page.
Here, the QuerySet of published articles will populate the template called 'index.html', but this template does not exist yet.
Let's take care of that now.

## Associated Template

We will create the _index.html_ file under a new _templates/_ folder, inside our _blog/_ application.


Templates created within an application will be automatically mapped by Django at the project level when the site is served, since the ```TEMPLATES``` settings in _simpleblog/settings.py_ have the parmeter ```'APP_DIRS'``` set to ```True```.

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

The template as defined here makes used of the ```'objects'``` variable passed by the 'index' view that contains the list of articles.

The last step to have our 'index' view operation is to connect it to the URL system, via a router.

## Routing System

In Django, it is good practice -and more elegant- to keep the applications' routing systems (**urls**) inside their respective applications.
The general routing system at the project level (in our case _simpleblog/urls.py_) will then import these configurations and add them to its central set of patterns.

Let's have the project's urls include the 'blog' _urls.py_ module,

```python
# simpleblog/urls.py
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('blog.urls')),
]
```  

and then create the _urls.py_ configuration inside _blog/_:

```python
# blog/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
```  

What we did here was telling the general _simpleblog/urls.py_ routing to use the _blog/urls.py_ configuration for all routes hitting the root of the domain (```r'^'```), and inside this configuration, having the calls to the root URL trigger the 'index' view.

We can give it a try right away (after starting the development server if it was not running): [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Details View and Templates

Now that we are familiar with the **url** + **view** + **template** architecture, let's create a similar structure to build individual pages for our articles.

This 'article' view will differ from the previous 'index' view in that it will require a unique parameter to identify an Article object.
We will use the _slug_ to that effect:

```python
# blog/views.py
from django.http import Http404
from django.shortcuts import render
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

The 'article' view indeed takes a _slug_ as a second argument in addition to the _request_ context, and attempts to fetch the Article object with such a value in its slug field.
Should the query fail, the view will return an **Http404**, an HTTP Response object with the special error code 404 (indicating that a resource was not found), with an explicit message.

The _article.html_ template will have the following form:

```html
<!-- blog/templates/article.html -->
<a href="{% url 'index' %}">← Back</a>
<div>
    <h1>{{ object.title }}</h1>
    <p>{{ object.body }}</p>
    <em>Created: {{ object.created }}{% if object.updated %} | Last edited: {{ object.updated }}{% endif %}</em>
</div>
```

This template is very similar to the _index.html_, except that it only applies to one 'article' object.
We also added a 'Back' button, that links to our index view using the 'url' template tag.

Let's add this view to the _blog/urls.py_ routing configuration:

```python
# blog/urls.py
...
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^articles/(?P<slug>\S+)$', views.article, name='details'),
]
```

The pattern recognized for this route is the ```/articles/``` prefix followed by a chain of characters (letters, numbers, underscores or hyphens), which is passed to the view as the 'slug' parameter.

We can try this view using the slug of one of our articles: [http://127.0.0.1:8000/articles/my-first-article](http://127.0.0.1:8000/articles/my-first-article).
Appending a character string that does not match any existing 'slug' value will result in a 404 error.

A last improvement on the _index.html_ template:

```html
<!-- blog/templates/index.html -->
...
    <h1><a href="{% url 'details' object.slug %}">{{ object.title }}</a></h1>
    <p>{{ object.body }}</p>
...
```

We just added a link to the 'details' view for each article, embedded in their title.
[http://127.0.0.1:8000](http://127.0.0.1:8000).

## Next...

We covered in this chapter the mechanics used to build and map interfaces with **urls**, **views** and **templates**.
However, the generated HTML code is pretty bare and does not make for a great experience for our users.
In the next chapter, we will take the time to add some [styling to our templates](training/5-StylingTemplates.md).