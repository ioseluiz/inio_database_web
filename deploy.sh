#!/usr/bin/env bash

# activate the virtual environment
source ~/venv/bin/activate

# cd into the project code
cd /var/www/inio_database_web

# pull
git pull

# Install the app dependencies
pip install -r requirements.txt

# Run the collect static command
python manage.py collectstatic --no-input

# put all other command that required for your specific app

# deactivate

# reload nginx
sudo systemctl reload nginx

# restart the gunicorn
sudo systemctl restart gunicorn