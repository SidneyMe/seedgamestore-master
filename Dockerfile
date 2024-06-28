# Use an official Python runtime as a parent image
FROM python:3.12.3

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code
COPY . /code

# Install dependencies
RUN pip install -r requirements.txt

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# Copy project
COPY . /code/

EXPOSE 8000

CMD [ "python3","manage.py","runserver", "0.0.0.0:8000" ]