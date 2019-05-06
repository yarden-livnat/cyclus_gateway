
FROM python:3.7 as build

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -U pip \
    && pip install -r /tmp/requirements.txt

COPY . /code
WORKDIR /code

ENTRYPOINT ["./scripts/entrypoint.sh"]
CMD ["python", "manage.py", "run"]

EXPOSE 80
EXPOSE 443
