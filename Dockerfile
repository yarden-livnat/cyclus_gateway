
FROM python:3.7 as build

COPY ./requirements /tmp/requirements
RUN pip install -U pip \
    && pip install -r /tmp/requirements/dev.txt

COPY . /code
WORKDIR /code

CMD ["python", "manage.py", "run"]
EXPOSE 5000
