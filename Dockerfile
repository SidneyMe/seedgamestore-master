# Use an official Python runtime as a parent image
FROM python:3.12.3

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_DATABASE_URL sqlite:///code/db.sqlite3
ENV DJANGO_ALLOWED_HOSTS localhost,127.0.0.1
ENV DJANGO_DEBUG False
ENV DJANGO_STATIC_ROOT /code/staticfiles
ENV DJANGO_MEDIA_ROOT /code/mediafiles
ENV DJANGO_SECRET_KEY "dv&32wcmdwps@nqe8eg12z=#&(nrij#y#vfxnm@eor+l&dm0wy"

# Set work directory
WORKDIR /code
COPY . /code

# Install dependencies
RUN pip install -r requirements.txt

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput

# Copy project
COPY . /code/

EXPOSE 8000

# Use Gunicorn to serve the application
CMD ["gunicorn", "diploma2024.wsgi:application", "0.0.0.0:8000"]