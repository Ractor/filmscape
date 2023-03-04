FROM python:3.11-alpine
EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app
RUN python manage.py migrate

ENTRYPOINT ["python"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]