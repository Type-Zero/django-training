[Index](../README.md)

# Python & Virtualenv on Mac OS X

This section intends to guide you through the setup of Python and Virtualenv (optionally Virtualenvwrapper) in a Mac OS X environment.

## Homebrew

Mac OS X is awesome, but out-of-the-box lacks one critical thing to be a powerful development environment: a centralized package manager.
Ubuntu distributions have _aptitude_ (the famous ```apt-get```), Fedora-based Linux systems have _RPM_ (with ```yum```), but Mac OS X does not have anything of that sort.

This is where __Homebrew__ comes in.
Hommebrew is your missing CLI package manager (that's even its official tagline: http://brew.sh/).

The only requirement to install it is __Ruby__, which conveniently comes pre-installed in OS X.

Let's install Homebrew. In the Terminal type-in:
```bash
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

During the installation, Homebrew will ask your for an administrator password, and it should the only time it does: all packages installed with Homebrew can be installed without 'root' permissions.

The first step after installing Homebrew in to run ```brew doctor```.
This command will look through the applications installed on your computer and determine whether some of them may enter in conflict with future Homebrew-installed packages.
In all cases, if any, _doctor_ gives you a recommendation on the approach to take to solve the potential conflict.
Nothing mandatory, but most often following those recommendations will save you a lot of headaches.

From now on, you can consider installing all your development tools, from SDKs to database engines, with Homebrew.
If it exists, it probably has an up-to-date formula on Homebrew.

_TIP: Should you be afraid of the all Command-Line-Interface aspect of Homebrew, you can have a look at CakeBrew (https://www.cakebrew.com), a minimalist GUI for Homebrew packages that simply sits on top of your Homebrew installation._

## Python(s)

__Python__ (https://www.python.org) comes pre-installed on Mac OS X systems, in its version 2.7.
In a Terminal window, type in ```python --version``` to check that.
```which python``` will show you which installation is identified by the 'python' command.
This will come in handy later on.

As nice as this is, __Python 3__ is becoming more and more popular and adopted for many platforms, and it would be great to have it running on our machine.
Also, __Python 2__ is updated fairly frequently, and the  version packaged with Mac OS X is not updated at the same rate.

Let's install both _python_ and _python3_ with Homebrew:

```bash
$ brew install python python3
```

You will want to run ```brew doctor``` right after this installation and follow any recommendation to make sure the newly installed _python_ won't conflict with the one pre-installed on the system.
Once that's done, you can now run ``` which python``` and ```which python3``` to check that your Terminal runs the correct executables.
Those should now point to '_/usr/local/bin/_' locations, which is where the Homebrew executables are stored.

```python --version``` and ```python3 --version``` will show you the exact version number of, respectively, Python2 and Python3.

## Virtualenv

When working on a lot of different Python projects, it can quickly become difficult to manage the various Python packages, extensions and libraries, especially if working with multiple version of Python (2 & 3).
__Virtualenv__ (https://pypi.python.org/pypi/virtualenv) is a Python library that can help with that: it allows you to create virtual Python environments for each of your projects, isolating the set of dependencies inside of them.

Let's install it using the Python Package manager __pip__:

```bash
$ pip install virtualenv
```

_TIP: 'Homebrew' is a package manager for all kinds of applications. 'PIP' is specifically a Python packages and libraries manager. Their use is not exclusive, it is complimentary!_

__At this point, you may choose to jump to the next section and start directly with 'virtualenvwrapper', which adds shortcut commands and simplifies the use of virtual environments, or continue here for more details on 'virtualenv'.__

TODO: "Pure" virtualenv (```source bin/activate```, 'env' location, etc...)

## Virtualenvwrapper

### Setup

__Virtualenvwrapper__ (https://virtualenvwrapper.readthedocs.org/en/latest/) is a set of tools complimentary to 'virtualenv', allowing for simpler commands and a centralized organization of virtual environments.
Virtualenvwrapper is also installed using 'pip':

```bash
$ pip install virtualenvwrapper
```

Virtualenvwrapper requires a very short setup to be fully operational: the defition of the ```WORKON_HOME``` environment variable and the addition of the 'virtualenvwrapper.sh' to the path of the Terminal.

```WORKON_HOME``` is the location where all your virtual environments will be stored.
The following setup chose "_~/.envs_", a hidden folder inside the user's home directory, but feel free to choose any location that makes sense for your architeture.
This folder may not exist yet when defined, we will take care of that right away.

The two parameters can be set 'on the fly' in the Terminal, or more permanently by adding them to a 'bash_profile' configuration.

- _Option 1, "Right here, right now":_
```bash
$ export WORKON_HOME=~/.envs
$ source /usr/local/bin/virtualenvwrapper.sh
```

- _Option 2, "I foresee a bright future":_
```bash
$ vi ~/.bash_profile
```
Once the file open CLI text editor, use the "i" key to enter insertion mode, and append the following to the document:
```bash
export WORKON_HOME=~/.envs
source /usr/local/bin/virtualenvwrapper.sh
```
Hit "esc" to leave insertion mode, then type in ":wq" to save and quit the _vi_ editor.
You will want to Quit and Restart the Terminal application for thos changes to be taken into account.

- _Option 1 & 2, "Anyways":_

Create the 'WORKON_HOME' folder if it does not exist already:
```bash
mkdir -p $WORKON_HOME
```

_TIP: Storing all the virtual environments in a central directory, like 'virtualenvwrapper' helps us doing here, highlights the concept that Python virtual environments and project directories are decoupled: you can access any environment from any project directory._

### Playing with Virtual Environments:

Let's create a first virtual environment, that we will call 'dev_python':
```bash
$ mkvirtualenv dev_python
```
After creating it, the virtualenvwrapper automatically _activates_ the environment: you are working inside this environment.
An environment is active if its name appears before the terminal prompt line, in our case: ```(dev_python)$ ```.

To leave the environment:
```bash
(dev_python)$ deactivate
```

To activate it again:
```bash
$ workon dev_python
```

A virtual environment inherit all the 'pip' packages from the system-wide python application, but all packages installed within this environment will only be available to it.
For example, let's install the famous 'pytz' package (a package to handle time zone-aware DateTime objects) in our development environment:
```bash
(dev_python)$ pip install pytz
```

A 'pip freeze' command will then list the installed packages:
```bash
(dev_python)$ pip freeze
```
As expected, our newly installed package appears in the list.
Now, leave the environment with ```deactivate``` and run the same ```pip freeze``` command: the package is not installed globally.

Our 'dev_python' environment is based on version 2 of Python, which is the default for virtualenvwrapper, but you can create a virtual environment based on Python 3 using the '-p' option:

```bash
$ mkvirtualenv -p python3 dev_python3
```

To check the Python version again inside the environment:
```bash
(dev_python3)$ python --version
Python 3.5.0
(dev_python3)$ workon dev_python
(dev_python)$ python --version
Python 2.7.10
```

_TIP: You can switch between environments using 'workon' without having to use 'deactivate'._


## Next...

This introduction to package management on Mac OS X hopefully gave you the bases to set up an efficient Python development environment.
Next, you may want to have a look at our [Django tutorial](training/1-Setup.md), which covers the use of the Django framework for the development of web applications.