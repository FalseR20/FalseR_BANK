# FalseR • 𝔹𝔸ℕ𝕂
#### Banking django server with PostgreSQL database

## Installation
1. git clone 
2. Create venv
   + python -m venv venv 
   + venv\Scripts\activate.bat
   + pip install -r requirements.txt

## Tuning
1. cd dj
2. python manage.py migrate
3. python manage.py createsuperuser
4. add currencies and default courses (BYN / CUR * 1 000 000) in admin panel

## Running
1. python manage.py runserver
