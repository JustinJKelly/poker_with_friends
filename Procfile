web: gunicorn poker_with_friends.wsgi --log-file -env DJANGO_SETTINGS_MODULE='poker_with_friends.settings'
web2: daphne poker_with_friends.routing:application --port $PORT --bind 0.0.0.0 -v2
