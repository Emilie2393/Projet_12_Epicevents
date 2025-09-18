# 🎉 EpicEvents  

**EpicEvents** is an ORM-based platform designed to manage **clients, contracts, and events**.  
It also includes a role-based user system, allowing different teams within the company to collaborate efficiently:  

- 👩‍💼 **Management**  
- 💼 **Sales**  
- 🛠️ **Support**  

---

## ✅ Prerequisites  
- 🐍 Have Python 3.12 or under installed. Python 3.13 may have some errors during the requirements installation.  
- 🗄️ Create a **MySQL database** named `epicevents`.  
- 📊 Set up a **Sentry account** (for error tracking and monitoring).  

---

## ⚙️ Configuration  
1. Before running the application, create a `.env` file in the project root with the following variables:  

```env
SECRET_KEY=your_custom_secret_key   # 🔑 Authentication token secret  
ADMIN=your_mysql_admin_name  # 🗄️ The admin name of your MySql database  
PASSWORD=your_mysql_password  # the password you choose for your MySql admin account  
SENTRY=your_sentry_dsn              # 🌐 DSN link from your Sentry account (SDK setup section)  
```  

The SECRET_KEY variable is useful for the authentication function. It acts as an encryption/signing key to generate and validate the access token.  
You can check for your ADMIN name with this MySql command:  

```mysql
SELECT User, Host FROM mysql.user;
```  

2. Create and activate your virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:  
```powershell
pip install -r requirements.txt
```  

---

## 🚀 Usage  

Launch the application:  
```powershell
python main.py
```  

### 📝 Workflow  

1. **Create a Management contributor** (required to add other contributors):  

![First menu](./images/logincli.PNG)

2. **Sales team**: create and update clients, as well as their associated contracts:  

![Clients menu](./images/clientsmenu.png)

3. **Management team**: create and update contracts:  

![Contracts menu](./images/contractcli.PNG)


4. **Sales team**: create events for clients with signed contracts.  
5. **Management team**: assign a Support contributor to each event.  
6. **Support team**: update and maintain event details.  

---
