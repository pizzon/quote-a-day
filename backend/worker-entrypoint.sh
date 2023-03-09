#!/bin/sh

until cd /src/backend
do
    echo "Waiting for server volume..."
done

cd ..
# run a worker :)
python -m celery -A quotes worker -l info -B