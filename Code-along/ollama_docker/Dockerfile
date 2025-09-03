FROM python:3.10

WORKDIR /code

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./app.py ./app.py

EXPOSE 8000
