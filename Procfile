release: python manage.py makemigrations users
python manage.py migrate
web: run-program waitress-serve --port=$PORT settings.wsgi:application
