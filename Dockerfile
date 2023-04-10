FROM python:3.10-alpine

WORKDIR /app

COPY ./swapi_app .

COPY ./requirements.txt .

RUN pip install -r requirements.txt

CMD python3 work_with_db.py && \
    python3 main.py
