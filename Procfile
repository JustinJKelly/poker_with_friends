web: gunicorn poker_with_friends.wsgi --log-file -
web2: daphne poker_with_friends.routing:application --port 8001
worker: python manage.py runworker channel_layer -v2
