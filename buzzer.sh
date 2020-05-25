#!/bin/bash
cd /opt/Jeopardy/
/home/eric/.local/bin/daphne -b 0.0.0.0 -p 10001 Jeopardy.asgi:application
