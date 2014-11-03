opfistula_case_manager
======================

An online management system for handling Fistula Medical Cases

Installation
---
* Install requirements
* Syncdb
* Install bower packages (https://github.com/nvbn/django-bower)
    * `python manage.py bower install`
    * `python manage.py collectstatic -l` create a symlink in static folder
* runserver