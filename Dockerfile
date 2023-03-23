FROM python:3.8.8-slim

WORKDIR usr/src/api

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/api

CMD ["bash", "./start.sh"]