FROM python:3.10.12-bullseye

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "application.py"]
