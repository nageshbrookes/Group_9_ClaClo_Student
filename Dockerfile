from python:3.9

WORKDIR /app

copy requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

copy ./app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]