#!/bin/bash

rm -rf dreamcatcherapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations dreamcatcherapi
python manage.py migrate dreamcatcherapi
python manage.py loaddata users.json
python manage.py loaddata dreamcatcherusers.json
python manage.py loaddata dreamtypes.json
python manage.py loaddata exercises.json
python manage.py loaddata medications.json
python manage.py loaddata moonphases.json
python manage.py loaddata stresses.json
python manage.py loaddata dreams.json
python manage.py loaddata dreammedications.json
python manage.py loaddata comments.json
python manage.py loaddata tokens.json