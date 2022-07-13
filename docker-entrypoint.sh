#!/bin/bash
rm -r Devprog
cd .
wget ${repo_link}

python3 new_client.py ${HOST} ${PORT} ${DB}
exec "$@"