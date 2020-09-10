FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code
RUN pip install --no-cache-dir -r requirements.txt
ADD . /code
CMD ["python" "manage.py runserver"]