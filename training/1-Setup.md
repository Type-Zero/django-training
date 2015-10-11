[← Previous](README.md) | [Index](README.md) | [Next →](training/2-Project.md)

# Setup

The following instructions assume you have set up **python3** with **pip**, **virtualenv** and **virtualenvwrapper** at the system level (OS X).

- Create a virtual environment based on Python 3.5:

```bash
$ mkvirtualenv -p python3 dj_training
```  

- Install Django:

```bash
(dj_training)$ pip install django
```  

- Check Python (3.5) and Django (1.8) version:

```bash
(dj_training)$ python --version
(dj_training)$ django-admin --version
```  

The command line instructions in the next chapters will assume that you work inside this virtual environment, unless otherwise specified.