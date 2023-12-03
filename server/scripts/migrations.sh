#!/bin/bash

/opt/venv/bin/python manage.py makemigrations
/opt/venv/bin/python manage.py makemigrations api
/opt/venv/bin/python manage.py migrate