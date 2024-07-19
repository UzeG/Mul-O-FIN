# Mul-O: Encouraging Olfactory Innovation in Various Scenarios Through a Task-Oriented Development Platform

This repository is the official implementation of Mul-O.
Welcome to try our new platform! And if it's useful for your work, please cite our UIST'2024 paper:)

Mul-O: Encouraging Olfactory Innovation in Various Scenarios Through a Task-Oriented Development Platform
Abstract：
Olfactory interfaces are pivotal in HCI, yet their development is hindered by limited application scenarios, stifling the discovery of new research opportunities. This challenge primarily stems from existing design tools focusing predominantly on odor display devices and the creation of standalone olfactory experiences, rather than enabling rapid adaptation to various contexts and tasks. Addressing this, we introduce Mul-O, a novel task-oriented development platform crafted to aid developers in navigating the diverse requirements of potential application scenarios. Mul-O facilitates the swift association and integration of olfactory experiences into functional designs, system integrations, and concept validations. Comprising a web UI for task-specific development, an API server for seamless third-party integration, and wireless olfactory display hardware, Mul-O significantly enhances the ideation and prototyping process in multisensory tasks. This was demonstrated in a 15-day workshop with 30 participants, resulting in seven innovative projects, underscoring Mul-O's efficacy in fostering olfactory innovation.


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
