#!/bin/bash

python ./manage.py qcluster &
python ./manage.py runserver localhost:8080
