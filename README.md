EPICEVENTS is an ORM platform to manage events. 

You need to create a MySql database named 'epicevents' first.

Then to run Epicevents app please create a .env file in the project folder and fill it like this :

SECRET_KEY = put here the secret key of your choice for the token of authentication of the current user
ADMIN = put the secret key for your mySql database according to this model : 'mysql+pymysql://admin:{ADMIN}@localhost/epicevents'

Copy requirements.txt with command ``pip install -r requirements.txt``

Now you can run python main.py to launch the script.

- Start to create a contributor from the management team to be able to create other contributors.
- Then you can create clients with the commercial team, update them after and update contracts attached to them.
- After you will be able to create and update contracts with the management team.
- Finally, you can create events with the commercial team for their clients who have signed their contract.
- Management team affect a support collaborator to each events previously created.
- Support team keep events correctly updated.

