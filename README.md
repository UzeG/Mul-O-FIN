# Mul-O: A Web-based Development Platform for Connecting More with Smell

This repository is the official implementation of Mul-O.

## ⚙️ Installation
Clone the Repository
```bash
git clone https://github.com/cheerlucy/Mul-O.git
```

## 💻 Web Application

### Enter the target folder
```bash
cd ./Mulo
```

### Using Conda Environment
1. Create the environment using the environment.yml file.
```bash
conda env create -f environment.yml
```

2. Activate the environment.
```bash
conda activate MulO
```

### Database
- Configuration
Open the `./Mulo/settings.py` file, and edit the `DATABASES` variable
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'atmospheror',  # your database name
        'USER': 'root',  # your database user
        'PASSWORD': 'admin123',  # your database password
        'HOST': 'localhost',  # your database host
        'PORT': '3306',  # your database port
    }
}
```

- Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Usage
```bash
python manage.py runserver 8080
```
