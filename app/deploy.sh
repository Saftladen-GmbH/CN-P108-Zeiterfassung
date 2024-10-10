#!/bin/sh

gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app()'