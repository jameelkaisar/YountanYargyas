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
- Unix
```
sudo apt update
sudo apt upgrade
sudo apt install python3-virtualenv
```
- Windows
```
pip install virtualenv
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
sudo apt install gunicorn
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
sudo service postgresql start
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
User=<username>
Group=www-data
WorkingDirectory=<repository_path>
ExecStart=<gunicorn_path> \
          --access-logfile - \
          --workers 2 \
          --bind unix:/run/gunicorn.sock \
          YountanYargyas.wsgi:application
[Install]
WantedBy=multi-user.target
```

Replace `username` by the output of `whoami` command

Replace `repository_path` by the path of clonned repository

Replace `gunicorn_path` by the output of `which gunicorn` command

#### Enabling gunicorn
```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

#### Configuring nginx
- YountanYargyas nginx file
```
sudo nano /etc/nginx/sites-available/YountanYargyas
```

```
server {
    listen <port>;
    server_name <ip>;

    client_max_body_size 300M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root <repository_path>;
    }

    location /media/ {
        root <repository_path>;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Replace `port` by the port on which you want to serve the website

Replace `ip` by the ip address on which you want to serve the website

Replace `repository_path` by the path of clonned repository

#### Enabling nginx
```
sudo ln -s /etc/nginx/sites-available/YountanYargyas /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

#### Configuring nginx (for IIAB only)
- capture.conf nginx file
```
sudo nano /etc/nginx/sites-available/capture.conf
```

Append the following to the capture.conf file
```
server {
    listen <port>;
    server_name <ip>;

    client_max_body_size 300M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root <repository_path>;
    }

    location /media/ {
        root <repository_path>;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```


Replace `port` by the port on which you want to serve the website

Replace `ip` by the ip address on which you want to serve the website

Replace `repository_path` by the path of clonned repository

#### Enabling nginx (for IIAB only)
```
sudo systemctl restart nginx
```

#### Additional points
- Add `Inbound Port Rule` on your server to allow external traffic
- Edit `ALLOWED_HOSTS` variable in `YountanYargyas/settings.py` file in the clonned repository to allow only specific domains
- Make sure `DEBUG` variable is set `False` in `YountanYargyas/settings.py` file in the clonned repository

#### Additional useful commands
- Restart gunicorn: `sudo systemctl daemon-reload && sudo systemctl restart gunicorn`
- Check gunicorn Status: `sudo systemctl status gunicorn.socket`
- Check gunicorn Logs: `sudo journalctl -u gunicorn`
- Restart nginx: `sudo systemctl restart nginx`

## Backup and Restore
### Backup
#### Automatic Backup
You can take partial or full backup directly from the Admin Section. The partial backup will take the backup of database only and the full backup will take the backup of database along with all the static files.

#### Manual Backup
First take the backup of `media` folder by copying it. Then take the backup of database using the following commands.

- UNIX
```
python3 manage.py dumpdata_utf8 > data.json
```
- Windows
```
python manage.py dumpdata_utf8 > data.json
```

### Restore
#### Manual Restore
First copy the `media` folder back. Then restore the database using the following commands.

- Unix
```
python3 manage.py migrate --run-syncdb
```
- Windows
```
python manage.py migrate --run-syncdb
```

Now run the following lines in the Django shell.
- Unix
```
python3 manage.py shell
```
- Windows
```
python manage.py shell
```
- You can skip this command if you use `python3 manage.py dumpdata_utf8 --exclude=contenttypes --exclude=auth.Permission > data.json` while taking the backup.

```
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
quit()
```

Now restore the database using the following command.
- Unix
```
python3 manage.py loaddata_utf8 data.json
```
- Windows
```
python manage.py loaddata_utf8 data.json
```

- Tip: You can also use default `dumpdata` and `loaddata` commands by setting `X` flag to `utf8` in python.
- Example: `python3 -X utf8 manage.py dumpdata > data.json`
