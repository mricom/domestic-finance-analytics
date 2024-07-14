FROM python:3.10
ENV PYTHONUNBUFFERED 1

COPY . /app

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r dev-requirements.txt

CMD ["/bin/bash", "-c", "devops/services/django/django_entrypoint.sh runserver-debug"]
