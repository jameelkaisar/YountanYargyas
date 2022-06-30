# YountanYargyas
Interactive learning website deployed using MeshNet in remote villages.


## About
Some text about this project: features, technical details, etc.


## Installation

### Requirements
- Python3
- pip
- git

### Testing

#### Clone the repository
```
git clone https://github.com/JameelKaisar/YountanYargyas.git
```

#### Change directory to project folder
```
cd YountanYargyas
```

#### Install `virtualenv`
```
pip install virtualenv
```

#### Add `virtualenv` to PATH (Unix only)
```
export PATH="$HOME/.local/bin:$PATH"
```

#### Create a virtual environment
```
virtualenv venv
```

#### Activate the virtual environment
- Unix
```
source venv/bin/activate
```
- Windows
```
venv\Scripts\activate.bat
```

#### Install the dependencies
```
pip install -r requirements.txt
```

#### Initialize the application
- Unix
```
python3 manage.py app_init
```
- Windows
```
python manage.py app_init
```
Enter superuser name and password

#### Start the application
- Unix
```
python3 manage.py run_lan --insecure
```
- Windows
```
python manage.py run_lan --insecure
```

#### Deactivate the virtual environment
```
deactivate
```

### Deployment (Ubuntu)

#### Installing requirements
```
sudo apt update
sudo apt upgrade
sudo apt install git python3-pip python-dev
sudo apt install libpq-dev postgresql postgresql-contrib
sudo apt install nginx
```

#### Clone the repository
```
git clone https://github.com/JameelKaisar/YountanYargyas.git
```

#### Change directory to project folder
```
cd YountanYargyas
```

#### Install the dependencies
```
pip install -r requirements.txt
```

#### Initialize the application
```
python3 manage.py app_init
```
Enter superuser name and password

#### Test the application
```
python3 manage.py run_lan --insecure
```

#### Setting up PostgreSQL database
```
sudo -i -u postgres
psql
CREATE DATABASE yountanyargyas;
CREATE USER admin WITH PASSWORD '#admin@db#';
ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE yountanyargyas TO admin;
\q
exit
```

#### Changing database to PostgreSQL
```
python3 manage.py db_postgre --name "yountanyargyas" --user "admin" --pass "#admin@db#"
python3 manage.py db_migrate
```

#### Test the application
```
python3 manage.py run_lan --insecure
```
