[← Previous](5-StylingTemplates.md) | [Index](README.md) | Next →

# Going Further

## New Model and Relation Fields

models.py
```python
# blogs/models.py
...
class Tag(models.Model):
    """
    Model for Tag
    """
    name = models.CharField(max_length=45)
    slug = models.SlugField(max_length=45, unique=True)
    
    def __str__(self):
        return self.name
```
m2m relationship
```python
# blogs/models.py
...
class Article(models.Model):
    ...
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('blog.Tag', related_name='articles')
    
    objects = ArticleQuerySet.as_manager()
    ...
```

admin.py
```python
# blog/admin.py
...
from .models import Article, Tag
...

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
```
migrate database

```python manage.py makemigrations``` + ```python manage.py migrate```

prefetch associated objects > bigger query but one-time.

```python
# blog/views.py
...
def index(request):
    articles = Article.objects.published().prefetch_related('tags')
    ...

def article(request, slug):
    try:
        article = Article.objects.filter(slug=slug).prefetch_related('tags').get()
    ...
```

display tags in index.html & article.html

```html
<!-- blog/templates/index.html & blog/templates/article.html -->
...
<div class="body body-list">{{ object.body }}</div>
{% if object.tags %}
<div class="tags">Tags: 
    {% for tag in object.tags.all %}
    <a href="#" class="tag small-tag"><span class="tagname">{{ tag.name }}</span></a>
    {% endfor %}
</div>
{% endif %}
<p class="date-info"><em>Created: {{ object.created }}{% if object.updated %} | Last edited: {{ object.updated }}{% endif %}</em></p>
...
```

style for tags

```css
/* blog/static/blog/css/styles.css */
...
.tags {
    margin-top:20px;
}
a.tag, .tag.small-tag, .tag.big-tag {
    display: inline-block;
    position: relative;
    height: 24px;
    line-height: 24px;
    vertical-align: middle;
    margin: 0 6px;
    padding-right: 6px;
    border: none;
    background-color: #000;
    color: #EEE;
}
.tag.big-tag {
    height: 36px;
    line-height: 36px;
    padding-right: 12px;
}
a.tag:hover {
    background-color: #FFF;
    color: #666;
}

/* Trick to create the 'bevel' shaped corners on left side of Tag Button */
a.tag:before, .tag.small-tag:before, .tag.big-tag:before {
    content: "";
    position: absolute;
    bottom:0;
    left:0;
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 7px 0 0 7px;
    border-color: transparent transparent transparent #EEE;
}

.tag.big-tag:before {
    border-width: 10px 0 0 10px;
}

a.tag:after, .tag.small-tag:after, .tag.big-tag:after {
    content: "";
    position: absolute;
    top:0;
    left:0;
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 7px 7px 0 0;
    border-color: #EEE transparent transparent transparent;
}

.tag.big-tag:after {
    border-width: 10px 10px 0 0;
}

.tag .tagname, .tag.small-tag .tagname, .tag.big-tag .tagname {
    display: inline-block;
    position: relative;
    height: inherit;
    margin:0;
    padding:0;
    padding-left: 24px;
    line-height: inherit;
    font-size: small;
}

.tag.big-tag .tagname {
    padding-left: 38px;
    font-size: medium;
}

/* Trick to create hole in Tag icon */
.tag .tagname:before, .tag.small-tag .tagname:before, .tag.big-tag .tagname:before {
    content: "";
    position: absolute;
    top: 7px;
    left: 7px;
    width: 10px;
    height: 10px;
    border-radius: 10px;
    background-color: #EEE;
}

.tag.big-tag .tagname:before {
    top: 10px;
    left: 10px;
    width: 16px;
    height: 16px;
    border-radius: 16px;
}
```

## Going further

build a query to get all articles for a given tag

new queryset shortcut method

```python
# blogs/models.py
...
class ArticleQuerySet(models.QuerySet):
    ...
    def tagged_with_slug(self, tag_slug):
        return self.filter(tags__slug=tag_slug)
...
```

new view

```python
# blog/views.py
...
from .models import Article, Tag
...
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
```

routing

```python
# blog/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^articles/(?P<slug>\S+)$', views.article, name='details'),
    url(r'^tags/(?P<tag_slug>\S+)$', views.tag, name='tag-selection'),
]
```

template

```html
<!-- blog/templates/selection.html -->
{% extends 'base-template.html' %}

{% block meta-title %}Tagged as "{{ tag.name }}"{% endblock %}

{% block content %}

<div class="article">
    <span class="tag-results">Results for tag</span> <span class="tag big-tag"><span class="tagname">{{ tag.name }}</span></span>
</div>

<div class="article">
    <p class="article-count">{% with count=objects.count %}{{ count }} Article{{ count|pluralize }}:{% endwith %}</p>
    <hr/>
    {% for object in objects %}
    <a class="selection-list" href="{% url 'details' object.slug %}">
        <span class="title">{{ object.title }}</span><span class="date-info"><em>Created: {{ object.created }}</em></span>
    </a>
    {% endfor %}
</div>
{% endblock %}
```

style

```css
/* blog/static/blog/css/styles.css */
...
.tag-results {
    font-size: x-large;
    font-weight: bold;
    vertical-align: middle;
    line-height: 36px;
}

.articles-count {
    margin-top: 20px;
}

a.selection-list {
    width: inherit;
    margin: 10px 0px;
    padding: 20px;
    display: block;
    color: inherit;
    text-decoration: none;
    border-radius: 5px;
    height: 36px;
    line-height: 36px;
    
}
a.selection-list:hover {
    background-color: #FFF;
}
.selection-list .title {
    font-size: x-large;
    font-weight: bold;
}
.selection-list .date-info {
    float: right;
    font-size: medium;
}
```

update links in index and details templates

```html
<!-- blog/templates/index.html & blog/templates/article.html -->
...
{% for tag in object.tags.all %}
<a href="{% url 'tag-selection' tag.slug %}" class="tag small-tag"><span class="tagname">{{ tag.name }}</span></a>
{% endfor %}
...
```

## Polish

remove back
```html
<!-- blog/templates/article.html -->
...
<div class="article">
    <h1>{{ object.title }}</h1>
    <hr/>
...
```

make title a link
```html
<!-- blog/templates/base-template.html -->
...
<nav class="navbar">
    <div class="title"><a href="{% url 'index' %}">My Django Blog</a></div>
</nav>
...
```  

details

```css
/* blog/static/blog/css/styles.css */
nav .title {
    ...
    color: #FFF;
    ...
}
nav .title a {
    color: inherit;
    text-decoration: none;
}
...
.article .body {
    text-align: justify;
    line-height: 25px;
    margin: 25px 0;
}
.article .body.body-list {
    overflow: hidden;
    text-overflow: ellipsis;
    max-height: 150px;
}
...
```