# FROM python:3.12

# RUN apt-get update && apt-get install -y \
#     python3-pip python3-dev build-essential libssl-dev libffi-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # # Upgrade pip
# RUN pip3 install --upgrade pip


# # Copy the code itself from context to the image
# # CMD [ "python manage.py runserver 0.0.0.0:8000" ]
# # RUN pwd
# WORKDIR /code


# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1


# COPY . .

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # RUN ls -lah

FROM python:3.10

# copy source and install dependencies
WORKDIR /code
COPY . /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python packages
RUN apt-get -y upgrade
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev build-essential libssl-dev libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install setuptools --upgrade
RUN python3 -m pip install wheel
# RUN python3 -m pip install -r requirements.txt
RUN pip install -r requirements.txt

# start server
EXPOSE 8000
STOPSIGNAL SIGTERM