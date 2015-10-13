[← Previous](5-StylingTemplates.md) | [Index](../README.md) | [Next →](#)

# Going Further

The previous chapters have led to a simple but fully functional site.
In this section, we will add a tagging functionality to label themes in our blog articles.
This will add a layer of complexity to the application by defining relations between models.

## New Model and Relation Fields

Let's create a 'Tag' model that will simply becomposed of a slug field (for URLs and searches) and a more explicit name field.
We will add it to _blog/models.py_:

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

The 'Tag' model is associated with 'Article' in a __Many-To-Many__ relationship, so that an Article can have multiple Tags, and a same Tage can be used for multiple Articles.
Let's add the _tag_ field to the 'Article' model:
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

The same way we added the 'Article' model to the __admin__ interface in _blog/admin.py_, let's create a ModelAdmin for our new entity, to give ourselves the ability to create and edit Tags via this interface:

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

Since we updated the _blog/models.py_, it is time to update the database schema.
We will run the ```python manage.py makemigrations``` command to generate a second migration file, *0002_auto_\[...\].py*.
A quick look at this file indicates that it depends on our initial migration file, and its instructions are pretty explicit: create our new 'Tag' model and add a new field to the 'Article'.

Let's now apply the migration by running ```python manage.py migrate```.
Our database is now ready to host the new 'Tag' entities.

You can now go to the __admin__ interface (http://127.0.0.1:8000/admin), create a few Tags and link them to Articles via the Article edition form.

## Interface Update

We now have a brand new entity, linked to the __admin__ back-end, but it is not yet showed to the user in any of our article views.
To take care of this, we will first need to edit our _blog/views.py_ to grab the tags associated with each article at the moment we query the database:

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

*TIP: The call to 'prefetch_related' asks Django to query the database for the associated Tags at the same time as it queries the Articles, in a single batch. 'prefetch_related' makes the overall query sligthly slower, but allows for a single database connection, which is crucial when your application scales up. If not for its use, each call to 'article.tags' in views and templates would generate an individual query for the related Tag objects.*

We also need to update our templates, to display the tags under the article body.
We will make the following update to both _blog/templates/index.html_ and _blog/templates/article.html_:

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

... and add styling attributes to make our Tags look awesome:

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

Now each Article appears with its set of Tags.
Pretty cool, right?

## Adding new functionalities

Having our Tags show up on the Article views is nice, but how about making tagging an actual functionality of our site?
For example, we could make the action of clicking a tag a way to access all articles associated with this tag.

We will start by creating a new __QuerySet__ method for the Article model, which will return all the entities associated with a tag's _slug_.
The method is defined as follow, in _blog/models.py_:

```python
# blogs/models.py
...
class ArticleQuerySet(models.QuerySet):
    ...
    def tagged_with_slug(self, tag_slug):
        return self.filter(tags__slug=tag_slug)
...
```

We will then have to create a new view to handle this functionality.
In response to a request which passes the tag _slug_ as an argument, we will return the list of Articles associated with the Tag in a new custom template.
The following is appended to _blog/views.py_:

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

Here we are using the 'values()' call at the end of our queryset.
The idea is to only select the fields that matter for our functionality: since we won't be displaying the entire articles in this new page, we can only select the _title_, _slug_ and _created_ fields of the Article objects, which is enough to create a list of Articles titles.
Users will be able to click each article to access its content.

By default, a QuerySet returns all the attributes of an object.
'values()', in the manner of a SQL __'SELECT'__ command, lets us pick the fields individually.

The next step is the creation of the template associated with this new view.
We will create a _'selection.html'_ template, inheriting our _blog/template/base-template.html_, under the same _blog/template/_ folder:

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

This template introduces a bunch of new HTML classes and elements, for which we will define styles in _styles.css_:

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

To make this view usable from the application, we need to add it to our __routing__ system, in _blog/urls.py_:

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

Finally, we can update the _index.html_ and _article.html_ templates, to transform the simple tags under the articles into links to our new _selection.html_ page.
As per the definition in _views.py_, the tag's slug is passed as an argument to the 'tag-selection' URL:

```html
<!-- blog/templates/index.html & blog/templates/article.html -->
...
{% for tag in object.tags.all %}
<a href="{% url 'tag-selection' tag.slug %}" class="tag small-tag"><span class="tagname">{{ tag.name }}</span></a>
{% endfor %}
...
```

Now not only our articles show up with themes labelled, but clicking those items now bring the user to a list of related articles, sharing the same Tag.
Pretty neat, right?

## Polishing the interface

In order to make the navigation experience consistent inside our application, let's get rid of the 'back' button in the article __details__ page, and instead make our title in the navigation bar a link to the __index__ page.
We will need to edit the _blog/templates/article.html_ file:

```html
<!-- blog/templates/article.html -->
...
<div class="article">
    <h1>{{ object.title }}</h1>
    <hr/>
...
```

as well as _blog/templates/base-template.html_:

```html
<!-- blog/templates/base-template.html -->
...
<nav class="navbar">
    <div class="title"><a href="{% url 'index' %}">My Django Blog</a></div>
</nav>
...
```  
We will make sure the title's appeareance does not change when adding the link, by updating the _styles.css_ settings:
```css
/* blog/static/blog/css/styles.css */
...
nav .title {
    ...
    color: #FFF;
    ...
}
nav .title a {
    color: inherit;
    text-decoration: none;
}
```

In this same stylesheet, we can also refine the appearance of the articles' body, by justifying the text and adding top and bottom margins.
Finally, it may be a good idea to only display the first few lines of each article in the __index__ views, keeping the full content for the __details__ view.
For now, we will simply handle it with CSS, by hiding the content of articles beyond the first four lines:

```css
/* blog/static/blog/css/styles.css */
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

## Next...

This chapter added depth to our application, both in terms of architecture complexity and set of functionalities.
The [next part](#) will focus on the improvement of the articles' content with advanced edition features using Django-Markdown.
This will be the opportunity to make use of a third party application and see how external modules interface with our Django project.