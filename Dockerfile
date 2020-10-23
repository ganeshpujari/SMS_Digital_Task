# Dockerfile

FROM python:3.7-buster

RUN apt-get update && apt-get install nginx vim -y --no-install-recommends

RUN mkdir -p /opt/metallics_optimizer
COPY requirements.txt /opt/metallics_optimizer/
WORKDIR /opt/metallics_optimizer
RUN pip install -r requirements.txt

# start server
EXPOSE 8000
CMD ["/opt/metallics_optimizer/", "python manage.py runserver" ]