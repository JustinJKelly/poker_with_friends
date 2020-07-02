web: gunicorn poker_with_friends.wsgi --log-file -
web2: daphne poker_with_friends.routing:application --port 6379 --bind 0.0.0.0 -v2
