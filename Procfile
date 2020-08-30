release: python manage.py migrate --no-input
web: daphne poker_with_friends.asgi:application --port $PORT --bind 0.0.0.0 -v2
web2: gunicorn poker_with_friends.wsgi --timeout 30 --preload
clock: python clock.py