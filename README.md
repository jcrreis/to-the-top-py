
# Setup Virtual Env

Create virtual for python
> python3 -m venv ~/envs/to-the-top-py

Load env
> source ~/envs/to-the-top-py/bin/activate

(to-the-top-py) should appear on prompt


# Install dependencies
> pip install -r requirements.txt

# Create the database
> mysql -u root -e "create database tothetop"

# Run migrations

Make migrations for development
> python manage.py makemigrations --settings=tothetop.settings_dev

Make migrations for production
> python manage.py makemigrations --settings=tothetop.settings_prod



Run migrations in development
> python manage.py migrate --settings=tothetop.settings_dev

Run migrations in production
> python manage.py migrate --settings=tothetop.settings_prod


# Run server 
Launch the server in development
>python manage.py runserver --settings=tothetop.settings_dev 

Launch the server in production
python manage.py runserver --settings=tothetop.settings_prod

Server should be available at http://127.0.0.1:8000/
