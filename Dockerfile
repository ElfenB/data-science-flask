FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip --no-cache-dir install -r requirements.txt

COPY . /app

# Set default executable
ENTRYPOINT ["python"]

EXPOSE 8080

CMD ["app.py"]
