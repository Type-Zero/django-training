[← Previous](training/1-Setup.md) | [Index](README.md) | [Next →](training/3-Application.md)

# Django Project

This chapter will cover the creation of a Django project, and detail its basic content.

## Project Creation

We will create a 'simpleblog' project using the following:

```bash
$ django-admin startproject simpleblog
$ cd simpleblog
```  

The ```startproject``` command is part of the _django-admin_ subset of Python commands, specific to the Django framework.
Run ```django-admin --help``` to get a list of the available functionalities.


Let's have a look a what this command just did:
 
Inside the Python module generated, two elements: **manage.py** and another **simpleblog** folder, in which we can find three files, **settings.py**, **urls.py** and **wsgi.py**.

- **manage.py** is a wrapper around _django-admin_ allowing you to work within the scope of your current project (see Django doc about [django-admin and manage.py](https://docs.djangoproject.com/en/1.8/ref/django-admin/)).
    From now on, we will use ```python manage.py``` instead of ```django-admin``` to run administration commands inside our project.


- **wsgi.py** contains the parameters to make our project a callable application.
    It will become important to deploy the site on a server.
    We don't need to worry about it right now.


- **settings.py** gathers all the settings and parameters of our Django project.
    In particular, ```INSTALLED_APPS``` details the applications that compose our project, and we can see that a few elements are there by default.
    ```DATABASES``` precises the nature and name of the database system.
    The default is _sqlite3_.
    Let's change the default name of the database to _database.sqlite3_, just for kicks:

    ```python
    # simpleblog/settings.py
    ...
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'database.sqlite3'),
        }
    }
    ...
    ```
    The ```ROOT_URLCONF``` parameter locates the main routing configuration file, which happens to have been created by ```startproject```: **urls.py**


- The **urls.py** file is the main routing configuration for our project.
    We can see that the URLs for Django's **admin** application are already taken care of here.


## Database Migration

Django requires a few default applications (see ```INSTALLED_APPS```), and those components rely on specific database tables.
Conveniently, the tables are already defined inside those applications, making their initialization very easy:

```bash
$ python manage.py migrate
```  

The execution of this command returns an explicit feedback:

```bash
Operations to perform:
  Synchronize unmigrated apps: messages, staticfiles
  Apply all migrations: auth, admin, contenttypes, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
  Installing custom SQL...
Running migrations:
  Rendering model states... DONE
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying sessions.0001_initial... OK
```  

Tables related to the _auth_, _admin_, _contentypes_ and _sessions_ modules are set up and populated as needed.

You will notice that the **database.sqlite3** file was created at the root level of our project (_simpleblog/_) after running the previous command.
This is our working database.
Here is the advantage of SQLite: the database is compact and portable.
Convenient for development, but we will see in later chapters that other options are available.

Our project is now set up and ready for its first test run.


## Development Server

Django comes with a built-in development server, that you can start with the following command:

```bash
$ python manage.py runserver
```  

By default, the development server runs on the localhost, 127.0.0.1, and on the port 8000.
You can modify those values by add them as an argument of the command: ```python manage.py runserver <your-ip-here>:<port>```.

We will stick to the default for now, and have a look at the site by opening a browser tab at the address [http://127.0.0.1:8000](http://127.0.0.1:8000).

Not much to it yet, but hey, at least it's working!

As hinted by **settings.py**'s ```INSTALLED_APPS``` and **urls.py**, the **admin** interface is already available by default at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).
Of course, we don't have any user defined at this point.
We will take care of this right now.

You can stop the server using **CONTROL+C**.


## Superuser Creation

The following management command lets us create a 'superuser' for our application:

```bash
$ python manage.py createsuperuser
```

The interactive shell will prompt you for a username, an email address and a password.

Once done, restart the server using ```python manage.py runserver```, and return to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).
This time, you will be able to log in with the newly created credentials, and access the administration interface.

Two authentication models are listed for the _auth_ module: **Groups** and **Users**.

While **Groups** is empty right now, **Users** should list at least one entry: the 'superuser' we just defined.

We don't need any other user or group for now, you can still have a look at the creation or edition forms for those entities.
Django's default **User** model actually has a lot more fields than the mandatory ones we defined via the command line interface.
**Users** can be assigned to **Groups**, which facilitates the management of multiple users and their permissions.

_NB: Generally, you will only want to use ```python manage.py createsuperuser``` once, to define your initial 'superuser', and then use the **admin** interface to create your other users if needed._


## Next...

At this point, we have set up the global frame for our project.
In the [next chapter](training/3-Application.md), we will start creating our own application.