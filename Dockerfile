FROM python:3.7-buster as builder
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt

FROM builder
WORKDIR /app
CMD ["python", "main.py"]