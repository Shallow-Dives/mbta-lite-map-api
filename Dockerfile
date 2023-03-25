FROM python:3.8.13-slim as build-stage

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
	      build-essential gcc

WORKDIR /usr/api
RUN python -m venv /usr/api/venv
ENV PATH="/usr/api/venv/bin:$PATH"

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.8.13-alpine3.16 as final
WORKDIR /usr/api
COPY --from=build-stage /usr/api/venv ./venv
COPY . .

ENV PATH="/usr/api/venv/bin:$PATH"
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers=4", "wsgi:app"]