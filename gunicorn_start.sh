#! /bin/bash
gunicorn run:app -c gunicorn.conf.py --preload