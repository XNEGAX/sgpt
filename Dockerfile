FROM python:3.10.7

ENV PYTHONUNBUFFERED 1
RUN mkdir /sgpt

WORKDIR /sgpt
COPY . /sgpt/

RUN pip install -r librerias.txt

CMD ["gunicorn", "-c","docker/gunicorn/conf.py","--bind",":8000","--chdir","config.wsgi:application"]