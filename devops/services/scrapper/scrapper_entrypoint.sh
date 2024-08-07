#!/bin/sh

export PYTHONPATH=$PYTHONPATH:/usr/src/app
export GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json

# Run the first script in the background
if [ "$1" = "subscriber" ]; then
    echo "Starting subscriber"
    python groceries/scrappers/subscriber.py
elif [ "$1" = "debug" ]; then
    echo "Starting publisher"
    python -m pip install debugpy
    python -m debugpy --listen  5679 groceries/scrappers/subscriber.py
fi
