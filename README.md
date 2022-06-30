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
export PATH="`pip show virtualenv | grep "Location:" | cut -d " " -f 2-`:$PATH"
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

#### Setting up gunicorn
```
pip install gunicorn
export PATH="`pip show gunicorn | grep "Location:" | cut -d " " -f 2-`:$PATH"
```

#### Testing gunicorn
```
gunicorn --bind 0.0.0.0:8000 YountanYargyas.wsgi
```

#### Configuring gunicorn
- gunicorn socket file
```
sudo nano /etc/systemd/system/gunicorn.socket
```

```
[Unit]
Description=gunicorn socket
[Socket]
ListenStream=/run/gunicorn.sock
[Install]
WantedBy=sockets.target
```

- gunicorn service file
```
sudo nano /etc/systemd/system/gunicorn.service
```

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target
[Service]
User=root
Group=www-data
WorkingDirectory=<repository_path>
ExecStart=<gunicorn_path> \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          YountanYargyas.wsgi:application
[Install]
WantedBy=multi-user.target
```

Replace `repository_path` by the path of clonned repository

Replace `gunicorn_path` by output of `pip show gunicorn | grep "Location:" | cut -d " " -f 2-` command

#### Enabling gunicorn
```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```
