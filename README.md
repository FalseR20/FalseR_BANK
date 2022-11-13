# FalseR • 𝔹𝔸ℕ𝕂

**Django** server with **PostgreSQL** database

## Installation

### Windows:

```shell
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Linux:

```shell
python3 -m venv venv
source venv\bin\activate
pip install -r requirements.txt
```

#### PostgreSQL

```shell
sudo -u postgres psql
```

```postgresql
create database falser_bank;
create user falser_bank with encrypted password '12345678';
grant all privileges on database falser_bank to falser_bank;
```

## Tuning

```shell
cd dj
python manage.py migrate
python manage.py createsuperuser
```

Also, you need to add currencies and default courses (CUR / BYN * 1 000 000) in admin panel

## Running

```shell
python manage.py runserver
```

## Or with using docker

```shell
sudo docker-compose build
sudo docker-compose up
```

## Screenshots

![](materials/screenshots/img.png "Main Window")
![](materials/screenshots/img_1.png "Registration window")
![](materials/screenshots/img_2.png "Cards")
![](materials/screenshots/img_3.png "Creating card")
![](materials/screenshots/img_4.png "Card page")
![](materials/screenshots/img_5.png "Result")
