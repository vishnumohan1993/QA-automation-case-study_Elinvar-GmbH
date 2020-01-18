FROM python:alpine3.11
COPY ./code /code
CMD python /code/log_reader.py