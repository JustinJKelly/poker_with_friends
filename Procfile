web: gunicorn poker_with_friends.wsgi --log-file -
web2: daphne poker_with_friends.routing:application --port 80 --bind 23.202.231.169 -v2
worker: python manage.py runworker channel_layer -v2
