FROM python:3.8-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /falser_bank
COPY . .
RUN pip install -r requirements.txt
#CMD python manage.py migrate
#CMD python manage.py createsuperuser --noinput --username admin --password 12345678
#CMD python manage.py runserver
