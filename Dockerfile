FROM python:3.12

RUN apt-get update && apt-get install -y chromium chromium-driver

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "scraper.py"]
