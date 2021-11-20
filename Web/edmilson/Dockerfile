FROM python:3.8-slim-buster
RUN mkdir /app
WORKDIR /app
COPY ./flag.txt /flag.txt
COPY ./requirements.txt /app
RUN pip install -r /app/requirements.txt
COPY . /app
EXPOSE 5000
ENTRYPOINT ["sh", "/app/entrypoint.sh"]