#!/bin/sh

export PYTHONPATH=$PYTHONPATH:/usr/src/app
export GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json

# Run the first script in the background
python groceries/scrappers/subscriber.py
