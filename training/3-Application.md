[← Previous](2-Project.md) | [Index](../README.md) | [Next →](4-ViewsAndTemplates.md)

# First Application

This chapter details the creation of an application module, and the definition of its _models_.
Basic use of the Django shell is also covered in this section.

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

We will cover each of those elements in more details in the rest of this tutorial, starting with the _models_ right now.

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
The **title** field is a standard chain of characters, while our **body** is a text field, an unlimited chain of characters allowing more flexibility.

The **slug** is a characters chain consisting exclusively of letters, numbers, underscores or hyphens.
A 'slug' is usually based on the title of the article and is used to build URLs.

**published** indicates whether the article should be published on our site.

The **created** and **updated** fields are date & time field marking, respectively, the creation and modification of an article.
The *auto_add_now* parameter lets Django set the date and time automatically when an object is created.
In the same fashion, *auto_now* lets it update the date and time field each time the object is modified.

The **\_\_str\_\_()** method defines what designates an Article object.
We logically use its title for that.

The **Meta** class sets generic metadata for our object.
*verbose_name* and *verbose_name_plural* are the names used to designate the object in the **admin** interface.
The *ordering* parameter defines the default order to be used to sort query-set results.

Now that the main model is defined, we need to actually create the associated entity in the database.
To do so, we will use the same ```python manage.py migrate``` command as seen in the [previous chapter](2-Project.md), but we first need to tell the project settings about our new module.

Let's add our 'blog' app to the ```INSTALLED_APPS``` in _simpleblog/settings.py_:

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

Once added to the ```INSTALLED_APPS```, the application will be taken into account by Django for a various set of processes, including the creation of migration files.
This is our next step:

```bash
$ python manage.py makemigrations
```

The output of this command is pretty explicit

```bash
Migrations for 'blog':
  0001_initial.py:
    - Create model Article
```

In the _blog/migrations/_ folder, the first migration file was created, ```0001_initial.py```.
This file contains the ORM python code that will be translated to database commands (**SQLite** in our case).

Now that the migration file is created, let's apply it:

```bash
$ python manage.py migrate
```
Our 'Article' model is now linked to a database entity.
We can add this model to the **admin** interface by editing the _blog/admin.py_ file:

```python
# blog/admin.py
from django.contrib import admin

from .models import Article

admin.site.register(Article)
```

This way, when reaching the **admin** interface at [http://127.0.0.1:8000](http://127.0.0.1:8000) (after starting the server using ```python manage.py runserver```), the 'Blog Articles' item appears under a new 'Blog' section.
This module enables you to add or edit Article objects via a simple form.
Go ahead and create a first Article, that you can directly set to 'published'.

The creation of the Article will redirect to a 'list' view of all the existing objects, where their title is used as an identifier.

Django lets you customize the appearance and behavior of a lot of components of the **admin** interface.
We will edit the _blog/admin.py_ file to make this interface more efficient:

```python
# blog/admin.py
from django.contrib import admin

from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'published')
    prepopulated_field = {'slug': ('title',)}

admin.site.register(Article, ArticleAdmin)
```  

Those modifications cover two elements:
- the 'list' display of our Articles now also show the creation date and publication status of the entries,
- the Article creation form now has the _slug_ field automatically populated based on the _title_'s value.
You can try this out by writing a new Article.
Let's keep it unpublished for now.

The **admin** module is a powerful interface for accessing and editing your data, but it is not the only way you can connect to the back-end of your system.
One other way to do that without the need to log into a web browser is the Django shell.

## Django Shell

Django comes bundled with a shell tool, which is fundamentally a Python prompt with a direct connection to your project's settings.
It allows you to import your models, views and parameters directly inside a terminal.

We will stop the development server (using **CONTROL+C**), and type in the following:

```bash
$ python manage.py shell
```

This opens up a pretty standard Python shell, which you can close by using **CONTROL+D**, or typing in ```> exit()```.
Let's try the following:

```bash
> from blog.models import Article
> Article.objects.all()
```
This set of commands imports the Article model from our 'blog' application, and uses the default _objects_ queryset to list all the existing Article entries.
This tool can be used to refine queries, such as:

```bash
> Article.objects.filter(published=True).all()
```  

This query filters the objects based on the _published_ field value, to only return the published Articles.
The results speak for themselves: when the first command return both of our Articles, the second only returned the first one since we left the second one unpublished.

Filters on query-sets are powerful, but Django also lets you define your own query-sets.

## Customized Query Sets

We will edit our _blog/models.py_ file to create a custom query set model:

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

and add this query set as a manager for our Article class:

```python
# blog/models.py
    ...
    updated = models.DateTimeField(auto_now=True)
    
    objects = ArticleQuerySet.as_manager()
    
    def __str__(self):
        return self.title
    ...
```
Let's try our new Query Set Manager.
If you haven't already, you will need to close the shell session (**CONTROL+D**) and re-open it with ```python manage.py shell```.

_Unlike the development server, the shell does not refresh its context automatically when a modification is made on a model or a view. Since we just updated our blog/models.py, we need to restart the shell to make sure the objects we work with are up to date._

```bash
> from blog.models import Article
> Article.objects.published()
```  

This effectively runs the same as our previous call to ```Article.objects.filter(published=True).all()```, but in a more elegant way.

_For such a trivial example, the advantage of using a custom QuerySet may seem small, but using straight out filters can rapidly become cumbersome, especially if chaining them and using them at multiple locations in the code. A personalized QuerySet acts as a shortcut for complex queries._

## Next...

This chapter saw the setup of the _models_ that will be the base of our site, and presented the tools used to interact with those entities from an administrator point of view.
The next step is to build a public interface to our site using [views and templates](4-ViewsAndTemplates.md).