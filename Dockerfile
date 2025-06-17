FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app .

ENV PYTHONPATH=/app

CMD ["python", "main.py"]