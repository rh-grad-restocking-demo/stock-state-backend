#!/bin/sh
python -m gunicorn -w 1 -b 0.0.0.0:8000 stock.wsgi:app &
python -m stock.consumer
