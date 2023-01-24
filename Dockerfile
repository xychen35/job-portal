FROM python:3.10

RUN mkdir /app
WORKDIR /app

ADD . /app/
ADD backend/requirements.txt requirements.txt

RUN apt update -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app/backend
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
