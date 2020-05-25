#!/bin/bash
cd /opt/Jeopardy
/home/eric/.local/bin/uwsgi --socket 0.0.0.0:8000 --protocol=http -w Jeopardy.wsgi
