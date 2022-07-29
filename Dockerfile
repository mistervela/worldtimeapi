FROM python:3.11.0a6-alpine3.15

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

#CMD ["app.app", "--host","0.0.0.0", "--port", "80"]
#CMD ["python", "./main.py", "--host","0.0.0.0", "--port", "80"]
CMD ["python", "./main.py", "--host","0.0.0.0", "--port", "80"]
