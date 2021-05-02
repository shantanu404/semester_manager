Semester Manager
================
A simple django website that keeps track of daily online classes and quizzes in a single place so that you don't have to
scour your group text messages everytime to just join a class.

### Dependencies
- `python 3.8`
- `pipenv`
- `django`
- `django-tinymce`

### How to customize and run locally?
Make sure to use Python 3.8 or higher versions. Install `pipenv` if not installed yet.
```bash
$ pip install pipenv
```

Setup a custom virtual environment using `pipenv`
```bash
$ pipenv --python 3
```

After that install the dependencies
```bash
$ pipenv install
```

Now if everything is installed we need to migrate the database. (ie. Create tables and fields in the database)
```bash
$ python manage.py migrate
```

This will take a while. Now, lets create our admin user
```bash
$ python manage.py createsuperuser
```

Now that everything is set, we can run the website locally using `manage.py`
```bash
$ python manage.py runserver
```
