FROM python:3.9
COPY website/requirements.txt /app/website/requirements.txt
RUN pip install --no-cache-dir -r /app/website/requirements.txt
COPY website /app/website
COPY bin /app/bin
COPY etc /app/etc
EXPOSE 8080
ENV PATH "$PATH:/app/bin"
WORKDIR /app/website
CMD ["python", "server.py"]
