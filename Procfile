web: gunicorn poker_with_friends.wsgi --log-file -
web2: daphne -b 0.0.0.0 -p 8001 poker_with_friends.asgi:application
worker: python manage.py runworker channel_layer -v2
