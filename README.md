
  

# eMenu

  
  
  

Rest API representing the restaurant menu. The functionalities include:

  

- creating menu with unique name

  

- adding any number of dishes to the menu

  

- sorting menus by dish count

  

- filtering menu cards by name

  

- user authorization

  

- auto-sending of emails to users about new and recently modified dishes

  
  
  

# Built with

  
  
  

- Django 3.1.5

  

- Django Rest Framework 3.12.2

  

- Celery

  

- Redis

  

- Postgres

  

- Docker

  

- docker-compose

  

- django all-auth

  

- django rest-auth

  

- django-filter

  

# Installing

##### Prerequisites

  

To run the project you'll need: **docker, docker-compose and some free space on your disc**

In the **src/** directory, where docker-compose.yaml file is, run:

  

    docker-compose up --build

  

**Loading fixtures:**

  

    docker-compose exec web python manage.py loaddata menus_initial_data users_initial_data

**Running tests** (You have to load the fixtures before running tests):

  

    docker-compose exec web python manage.py test

  

**App will be available at:**

  

    localhost:8000/

**To check the swagger documentation, navigate to:**

  

    localhost:8000/swagger/

**All menus will be available at:**

  

    localhost:8000/menus/
**Example menu`s detail card:**

    localhost:8000/menus/Italian Menu/

**Logging in:**

Use one of the existing account:

  

**Bob:**

    email: bob@emenu.com
    
    password: example123

  

**Alice:**

    email: alice@emenu.com

    password: example123

  

**With existing accounts, you can log in at:**

  

    localhost:8000/auth/login/

**You can also create your own account at:**

  

    localhost:8000/auth/registration/

  

When you are logged in, you can add new menus and dishes, and see all the details of database records.

  

**All dishes will be visible for registered users, at:**

  

    localhost:8000/dishes/

**Example API calls with filters:**

Order menus by name in descending order:

    localhost:8000/menus/?ordering=-name
Search for menu with word 'Italian' in the name:

    localhost:8000/menus/?search=Italian
Search for menu with letter 's' in the name:

    localhost:8000/menus/?search=s
Search for menus created between two dates:

    localhost:8000/menus/?created_after=2021-01-24 23:35&created_before=2021-01-25 23:36&updated_after=&updated_before=
