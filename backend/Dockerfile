FROM python:buster

WORKDIR /src
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# This will allow you to pass in credentials.
# The default values are for local development
# but can override these when you run the container.
# It's not completely secure, but good enough.
ENV SECRET_KEY=abc123
ENV DEBUG=True

COPY . .

#RUN python manage.py makemigrations && python manage.py migrate

RUN chmod +x /src/server-entrypoint.sh
RUN chmod +x /src/worker-entrypoint.sh

