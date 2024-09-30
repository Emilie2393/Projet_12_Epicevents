EPICEVENTS is an ORM platform to manage events. 

You need to create a MySql database named 'epicevents' first.

Then to run Epicevents app please create a .env file in the project folder and fill it like this :

SECRET_KEY = put here the secret key of your choice for the token of authentication of the current user
ADMIN = put the secret key for your mySql database according to this model : 'mysql+pymysql://admin:{ADMIN}@localhost/epicevents'

Now you can run python main.py to launch the script.
