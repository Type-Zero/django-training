[← Previous](4-ViewsAndTemplates.md) | [Index](../README.md) | [Next →](6-NewModelAndRelations.md)

# Styling our Templates

This chapter will describe Django templates' **inheritance** and **block** functionalities.
It will also present a very basic CSS stylesheet, to demonstrate the integration of **static** files.

## Template Improvements

The templates defined so far for our 'index' and 'details' views are limited to the strict minimum.

Let's add some basic HTML components to our _blog/templates/index.html_ to build the structure of an actual web page:

```html
<!-- blog/templates/index.html -->
{% load static from staticfiles %}
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>Django Blog</title>
        <link rel="stylesheet" href="{% static 'blog/css/styles.css' %}">
        <!--[if lt IE 9]>
            <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
        <![endif]-->
    </head>
    <body>
        <div class="container">
            <nav class="navbar">
                <div class="title">My Django Blog</div>
            </nav>
            
            {% for object in objects %}
            <div class="article article-list">
                <h1><a href="{% url 'details' object.slug %}">{{ object.title }}</a></h1>
                <hr/>
                <div class="body body-list">{{ object.body }}</div>
                <p class="date-info"><em>Created: {{ object.created }}{% if object.updated %} | Last edited: {{ object.updated }}{% endif %}</em></p>
            </div>
            {% endfor %}
            
        </div>
    </body>
</html>
```

We embedded our set of articles ```<div>``` inside a ```<header>``` + ```<body>``` structure, and added a navigation bar on top of it.
The header contains a set of meta-data parameters, used by the client's browser to parse HTML files.

In addition to that, we also added a few classes to the elements of our initial code, to be interpreted and formatted by the stylesheet.

One new type of template tag makes its appearance in this code: the ```{% static %}``` tag.
This tag is used by the template engine to load **static** resources (typically Javascript, CSS, images and fonts).
In the same fashion as the templates themselves, the static folders are collected in each individual application when they are served (_we will learn in later chapters that the situation is slightly different when working outside of a development environment_).

```{% static %}``` tags share a similar syntax with the ```{% url %}``` tags: the second argument indicates the path of the file to serve.
While ```{% url %}``` tags are part of the templates' default configuration, ```{% static %}``` must be imported from a set of additional functionalities, hence the ```{% load static from staticfiles %}``` at the start of the file.

We just told our template we would want to import a 'blog/css/styles.css' file.
Let's get to work!

## Cascading Style Sheets

As suggested in the previous section, we will place our _static/_ directory inside the _blog/_ module, and add two folders nested within it: _static/blog/css/_, where we will create the _styles.css_ file.
This file will take care of the styling instructions for our bare HTML template, starting with a nice font!

```css
/* blog/static/blog/css/styles.css */
@import url(http://fonts.googleapis.com/css?family=Lato:300,400,700,900);

body {
    font-family: 'Lato', Helvetica, Arial, sans-serif;
    box-sizing: border-box;
}

.container {
    max-width: 840px;
    min-width: 480px;
    padding: 0 20px;
    margin: auto;
}

nav {
    width: inherit;
    padding: 10px 20px;
    margin: 20px auto;
    border-radius: 5px;
    background-color: #000;
}
nav .title {
    width: inherit;
    color: #EEE;
    font-weight: bold;
    font-size: large;
}

.article {
    width: inherit;
    border-radius: 5px;
    margin: 20px 0;
    padding: 10px 20px;
    background-color: #EEE;
}
.article h1 {
    margin: 10px 0;
}
.article h1 a {
    color: #000;
    font-weight: bold;
    font-size: xx-large;
    text-decoration: none;
}
.article .date-info {
    color: #666;
    font-size: smaller;
}
.article  .body {
    text-align: justify;
}
.article .body.body-list {
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 25px;
    max-height: 100px;
}
.article hr {
    border: 0;
    height: 1px;
    background: #000;
}
```

This Cascade Style Sheet is only a basic example, feel free to play around with those parameters or import your own themes in it.

Our 'index' page starts to look pretty decent at this point: [http://127.0.0.1:8000](http://127.0.0.1:8000).

The only problem is that these styles only apply to this specific page, and the 'details' pages for our individual articles don't look as good as this one.
We could go through the same process of updating the _article.html_ template with the same elements we added to _index.html_, but instead this is the opportunity to have a look at Django's **templates inheritance** functionality.

## Template Inheritance

The idea here is to gather the elements we want to be common to all our templates inside a 'base' template, and have our templates inherit this object while having specific content.
The way Django goes about this is by using ```{% block %}``` tags, encapsulating content that can be overridden by child templates.

Let's create our base template, _blog/templates/base-template.html_:

```html
<!-- blog/templates/base-template.html -->
{% load staticfiles %}
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>Django Blog - {% block meta-title %}{% endblock %}</title>
        <link rel="stylesheet" href="{% static 'blog/css/styles.css' %}">
        <!--[if lt IE 9]>
            <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
        <![endif]-->
        {% block stylesheets %}{% endblock %}
    </head>
    <body>
        <div class="container">
            <nav class="navbar">
                <div class="title">My Django Blog</div>
            </nav>
            {% block content %}{% endblock %}
        </div>
    </body>
    {% block scripts %}{% endblock %}
</html>
```
We defined four ```{% blocks %}``` that can be populated in child templates.

Let's now update _blog/templates/index.html_ to extend this base template:

```html
<!-- blog/templates/index.html -->
{% extends 'base-template.html' %}

{% block meta-title %}Index{% endblock %}

{% block content %}

{% for object in objects %}
<div class="article article-list">
    <h1><a href="{% url 'details' object.slug %}">{{ object.title }}</a></h1>
    <hr/>
    <div class="body body-list">{{ object.body }}</div>
    <p class="date-info"><em>Created: {{ object.created }}{% if object.updated %} | Last edited: {{ object.updated }}{% endif %}</em></p>
</div>
{% endfor %}

{% endblock %}
```

As we can see here, the ```{% block meta-title %}``` and ```{% block content %}``` blocks are overridden in the _index.html_ template to display the appropriate content.
Those changes are transparent for the final HTML code: [http://127.0.0.1:8000](http://127.0.0.1:8000).

With this structure in place, we can easily extend the base template to _blog/templates/article.html_:

```html
<!-- blog/templates/article.html -->
{% extends 'base-template.html' %}

{% block meta-title %}{{ object.title }}{% endblock %}

{% block content %}
<div class="article">
    <a class="back" href="{% url 'index' %}">← Back</a>
    <h1>{{ object.title }}</h1>
    <hr/>
    <div class="body body-list">{{ object.body }}</div>
    <p class="date-info"><em>Created: {{ object.created }}{% if object.updated %} | Last edited: {{ object.updated }}{% endif %}</em></p>
</div>
{% endblock %}
```

In addition to the tags definition, we slightly modified some of the initial elements, moving the 'Back' ```<a>``` link inside the article ```<div>``` and adding classes for styling.

Let's update our _styles.css_ to handle the 'Back' links styling:

```css
/* blog/static/blog/css/styles.css */
...
.article .back {
    font-size: smaller;
    color: #000;
    text-decoration: none;
}
```

## Next...

This chapter covered the main features of the Django **Template** engine, helping us to work on the design of the interface.
[Next](6-NewModelAndRelations.md), we will return to core elements of Django, by adding new **models** to our application and managing relations between entities.