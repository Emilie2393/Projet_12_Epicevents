EPICEVENTS is an ORM platform to manage events. You will be hable to handle clients, contracts and events but also to create new users to manage these data according to their role in the company :  

- Management
- Commercial
- Support

  
__You need to create a MySql database named 'epicevents' first and a Sentry account online.__

Then to run Epicevents app please create a .env file in the project folder and fill it like this :  

SECRET_KEY = put here the secret key of your choice for the token of authentication of the current user  
ADMIN = put the secret key for your mySql database according to this model : 'mysql+pymysql://admin:{ADMIN}@localhost/epicevents'  
SENTRY = put the DSN link to set up your Sentry account with Epicevents app. You will find it in the SDK Setup of your Sentry account.  

Copy requirements.txt with command ``pip install -r requirements.txt``  

Now you can run ``python main.py`` to launch the script.  

  
- Start to create a contributor from the management team to be able to create other contributors.  

![logincli](https://github.com/user-attachments/assets/0c148f67-9814-4d2d-b6a1-805df865d5a7)  
  
- Then you can create clients with the commercial team, update them after and update contracts attached to them.

![createcli](https://github.com/user-attachments/assets/0035154e-afc4-4625-ac05-2e74f56473e7)  
  
- After you will be able to create and update contracts with the management team.  

![contractcli](https://github.com/user-attachments/assets/d786fb31-e114-4629-b1ab-642208db39da)  

- Finally, you can create events with the commercial team for their clients who have __signed their contract__.
- Management team affect a support collaborator to each events __previously__ created.
- Support team keep events correctly updated.

