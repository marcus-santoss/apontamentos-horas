FROM python:alpine

WORKDIR /app
VOLUME providers

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "app.py"]
