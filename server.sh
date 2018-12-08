#!/bin/bash
if [ $FLASK_APP != server.py ]
then
	export FLASK_APP=server.py
fi
if [ $FLASK_ENV != production ]
then
	export FLASK_ENV=production
fi
flask run