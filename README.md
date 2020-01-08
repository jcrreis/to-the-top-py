
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
Create migrations for users
> python manage.py makemigrations users

Run migrations
> python manage.py migrate

# Run server
Launch the server
>python manage.py runserver

Server should be available at http://127.0.0.1:8000/
