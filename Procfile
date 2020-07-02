web: gunicorn poker_with_friends.wsgi --log-file -
web2: daphne poker_with_friends.routing:application --port 8001 --bind 0.0.0.0 -v2
worker: python manage.py runworker channel_layer -v2
