FROM python:3.11-alpine
EXPOSE 8000
WORKDIR /app

ARG FILMSCAPE_DB_NAME
ARG FILMSCAPE_DB_USER
ARG FILMSCAPE_DB_PASSWORD
ARG FILMSCAPE_DB_HOST
ARG FILMSCAPE_DB_PORT

COPY requirements.txt /app
RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

COPY . /app

ENTRYPOINT ["sh"]
CMD ["start.sh"]