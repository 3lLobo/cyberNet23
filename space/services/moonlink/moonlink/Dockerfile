FROM python:3.12-rc-slim

RUN apt-get update && apt-get install -y \
    socat

WORKDIR /opt/moonlink/
COPY requirements.txt /opt/moonlink/requirements.txt
RUN pip install -r requirements.txt

RUN mkdir -p /tmp/moonlink
RUN chmod 777 /tmp/moonlink

COPY moonlink.py /opt/moonlink/moonlink.py
COPY mooncomms.py /opt/moonlink/mooncomms.py

CMD ["/usr/bin/socat", "tcp4-listen:3000,reuseaddr,fork", "exec:/opt/moonlink/moonlink.py,stderr,pty,echo=0,su=nobody"]
