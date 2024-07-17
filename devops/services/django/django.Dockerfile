
FROM python:3.10
ENV PYTHONUNBUFFERED 1

COPY . /app

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r dev-requirements.txt

RUN chmod a+x devops/services/django/django_entrypoint.sh

# Verify permissions (optional step for debugging)
RUN ls -l devops/services/django/django_entrypoint.sh

CMD ["/bin/bash", "devops/services/django/django_entrypoint.sh",  "runserver-debug"]
