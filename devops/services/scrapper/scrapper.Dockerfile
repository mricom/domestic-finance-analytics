FROM python:3.10

ENV PYTHONUNBUFFERED 1


COPY . /app

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r dev-requirements.txt

# Install Java
RUN apt-get update && apt-get install -y default-jre

RUN chmod a+x devops/services/scrapper/scrapper_entrypoint.sh
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/service-account-key.json"


CMD ["/bin/bash", "devops/services/scrapper/scrapper_entrypoint.sh"]
