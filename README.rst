Ayen App
=========

Pre-interview technical assessment task!

.. image:: https://img.shields.io/badge/built%20with-Django%20-ff69b4.svg
     :target: https://www.djangoproject.com/
     :alt: Built with Django  


:License: MIT

Project Description
^^^^^^^^^^^^^^^^^^^^^

Write a project in Python Django, that has the following functionality:
 Signup (parameters: email and password)
 Login (parameters: email and password)
 Upload Metadata (parameters: name and string)
 Get all Metadata
 Get Metadata (parameter: name)
 Upload Document (parameters: name and file)
 Get Documents
 Get Document (parameter: name)
All the endpoints except Signup and Login are authenticated using JWT.


Project Setup
^^^^^^^^^^^^^

To run the project on local machine you have to setup python3 and postgresql first::

    $ sudo -u postgres psql
    $ postgres=# create database mydb;;
    $ postgres=# create user myuser with encrypted password 'mypass';
    $ postgres=# grant all privileges on database mydb to myuser;
    $ postgres=# \q
    $ git clone https://github.com/AbdelrahmanRabiee/ayenapp.git
    $ mkdir venv/
    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ nano ayenapp/.env
    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py runserver


.env structure
^^^^^^^^^^^^^

    DB_NAME='mydb'
    DB_USER='myuser'
    DB_PASSWORD='mypass'
    SECRET_KEY=herhherhehkerhuifreyy4y54y33gg33gy3y3
    DEBUG=True
    ALLOWED_HOSTS=0.0.0.0,127.0.0.1
    CELERY_BROKER_URL='redis://localhost:6379'
    CELERY_RESULT_BACKEND='redis://localhost:6379' 


Project Testing
^^^^^^^^^^^^^^^

     To run test cases do below commands::

          $ python manage.py test users.tests.test_api     
