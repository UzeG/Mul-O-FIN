# Mul-O: Encouraging Olfactory Innovation in Various Scenarios Through a Task-Oriented Development Platform

This repository is the official implementation of Mul-O.

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
### Contributing
We welcome contributions from the community. If you are interested in contributing, please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Commit your changes (git commit -m 'Add new feature').
4. Push to the branch (git push origin feature-branch).
5. Open a pull request.

### Contributors

Peizhong Gao, Fan Liu, Yuze Gao, Qi Lu

### Citation
If you find this project useful in your research or development work, please cite our paper:
[The official citation information will be updated after the paper getting published.]

@article{mulo2024,
  title={Mul-O: Encouraging Olfactory Innovation in Various Scenarios Through a Task-Oriented Development Platform},
  author={Peizhong Gao, Fan Liu, Di Wen, Yuze Gao, Linxin Zhang,Yu Zhang, Shao-en Ma, Qi Lu, Haipeng Mi and Yingqing Xu},
  booktitle={Proceedings of the 37th annual acm symposium on user interface software and technology},
  year={2024},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  pages={XX-XX},
  doi={10.1234/jash.2024.5678}
}

### License
This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0).

You are free to:

*Share* — copy and redistribute the material in any medium or format

*Adapt* — remix, transform, and build upon the material

Under the following terms:

*Attribution* — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

*NonCommercial* — You may not use the material for commercial purposes.

*ShareAlike* — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

For commercial use, please contact us to obtain a license.

### Contact
For any inquiries or further information, please contact us at:

Email: luq@mail.tsinghua.edu.cn

Website: _thfl.tsinghua.edu.cn_

Thank you for your interest in our project!

