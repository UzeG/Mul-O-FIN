# Mul-O web

A Web-based Development Platform for Connecting More with Smell

## 👨‍💻 Todo
[ ] Online demo of Mul-O
<br>
[x] Code of Mul-O (completed)
<br>

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/cheerlucy/Mul-O.git
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

## 🛠️ Usage
```bash
python manage.py runserver![img.png](img.png)
```