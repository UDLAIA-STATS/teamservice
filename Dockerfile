FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apt-get update \
 && apt-get install -y --no-install-recommends libpq-dev gcc bash \
 && pip install --no-cache-dir -r /app/requirements.txt \
 && apt-get purge -y --auto-remove gcc \
 && rm -rf /var/lib/apt/lists/*

# Copiamos app, .env y el settings.ini que mencionaste
COPY . /app
COPY .env /app/.env
COPY settings.ini /app/settings.ini

COPY docker/entrypoint_team.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8020

CMD ["/app/entrypoint.sh"]
