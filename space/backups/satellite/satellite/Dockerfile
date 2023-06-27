FROM python:3.12.0b3

WORKDIR /opt/satellite/

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

ADD . /opt/satellite/
RUN chown -R nobody:nogroup /opt/satellite

CMD ["./satellite_service.py"]
