FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY flask_app.py .

EXPOSE 5000

CMD ["python3", "flask_app.py"]
