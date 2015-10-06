[← Previous](2-Project.md) | [Index](README.md) | Next →

# First Application

This chapter details the creation of an application module, and the definition of its _models_ and _views_.
Basic use of the Django shell is also covered here.

## Application Creation

We will start up by creating an application module called 'blog'.
You will want to run the following command at the root of your project, inside the first _simpleblog/_ folder.

```bash
$ python manage.py startapp blog
```  

The ```startapp``` command created a new _blog/_ python module in which the main Django components were generated:
- **admin.py** is where we will register the models to be added to the _admin_ interface.
- **migrations/** will contain the migration files, keeping track of the database structure at every step of the development.
- **models.py** defines the database entities that will be the base for our application.
- **tests.py** will hold the tests used to verify the application.
- **views.py** is the place where the views are defined, the logic used to render HTTP response objects.

We will cover each of those elements in more details in the rest of this chapter.

## Models

Let's create our first model. What more original for a 'blog' application than an 'Article' entity?
We will edit _blog/models.py_:

```python
# blog/models.py
from django.db import models

class Article(models.Model):
    """
    Model for Blog Article.
    """
    title = models.CharField(max_length=90)
    body = models.TextField()
    slug = models.SlugField(max_length=90, unique=True)
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Blog Article'
        verbose_name_plural = 'Blog Articles'
        ordering = ['-created']
```
The **title** field is a standard chain of characters, while our **body** is a text field, an unlimited chain of character allowing more flexibility.

The **slug** is a character chain consisting exclusively of letters, numbers, underscores or hyphens.
A 'slug' is usually based on the title of the article and is used to build URLs.

**published** indicates whether the article should be published on our site.

**created** and **updated** are date & time field marking, respectively, the creation and modification of an article.
The *auto_add_now* parameter lets Django set the date and time automatically when an object is created.
In the same fashion, *auto_now* lets it update the date and time field each time the object is modified.

The **\_\_str\_\_()** method defines what designates an Article object.
We logically use its title for that.

The **Meta** class defines generic metadata for our object: *verbose_name*, *verbose_name_plural*, *ordering* blah blah blah...

* * *
DRAFT
* * *

Add blog to installed apps

```python
# simpleblog/settings.py
...
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
)
...
```

Create initial migration:

```bash
$ python manage.py makemigrations
```
```bash
Migrations for 'blog':
  0001_initial.py:
    - Create model Article
```

Migration created, let's apply:

```bash
$ python manage.py migrate
```

Register model to admin.py:
```python
# blog/admin.py
from django.contrib import admin

from .models import Article

admin.site.register(Article)
```

Customize the Article model admin:

```python
# blog/admin.py
from django.contrib import admin

from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "created")
    prepopulated_field = {"slug": ("title",)}

admin.site.register(Article, ArticleAdmin)
```  

## Shell

```bash
$ python manage.py shell
```

```bash
> from blog.models import Article
> Article.objects.all()
> Article.objects.filter(published=True).all()
```

Custom QuerySet

```python
# blog/models.py
from django.db import models

class ArticleQuerySet(models.QuerySet):
    """
    Custom QuerySet for Blog Article model
    """
    def published(self):
        return self.filter(published=True)
...
```

```python
# blog/models.py
    ...
    updated = models.DateTimeField(auto_now=True)
    
    objects = ArticleQuerySet.as_manager()
    
    def __str__(self):
        return self.title
    ...
```
Let's try our new QuerySet Manager:
```python manage.py shell```

```bash
> from blog.models import Article
> Article.objects.published()
```
