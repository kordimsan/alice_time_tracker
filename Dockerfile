FROM python:3.7-alpine3.9

WORKDIR /app
COPY . /app

EXPOSE 5000

# RUN pip install -r requirements.txt
RUN pip install poetry

RUN poetry install --no-dev --no-ansi

CMD FLASK_APP=api.py flask run --host="::"
