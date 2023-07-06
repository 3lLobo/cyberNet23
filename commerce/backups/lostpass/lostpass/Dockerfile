# pull official base image
FROM python:3.8

# set work directory
WORKDIR /opt/lostpass

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Create /data dir as read+write
RUN mkdir /data -p -m a=rw

# Make symlink for to-be-mounted data
RUN ln -s /data-ro/ai /data/ai
RUN chown -R root:root /data
RUN chmod -R 777 /data

# Add logging file
RUN touch /var/log/django.log
RUN chown -R nobody:nogroup /var/log/django.log

# copy project
ADD . / /opt/lostpass/
RUN chown -R nobody:nogroup /opt/lostpass

CMD ["python", "manage.py", "runserver", "0.0.0.0:3005"]