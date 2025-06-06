FROM python:3.9-slim

WORKDIR /

COPY /app/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app .

CMD ["python", "crudAlunos.py"]