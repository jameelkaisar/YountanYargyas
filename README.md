# YountanYargyas
Interactive learning website deployed using MeshNet in remote villages.


## About
Some text about this project: features, technical details, etc.


## Installation

### Testing

#### Installing requirements
```
sudo apt update
sudo apt upgrade
sudo apt install git python3-pip python-dev
```

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

### Add `virtualenv` to PATH (Unix only)
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
python3 manage.py run_lan
```
- Windows
```
python manage.py run_lan
```

#### Deactivate the virtual environment
```
deactivate
```
