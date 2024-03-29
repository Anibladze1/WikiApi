FROM python:3.10.0-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--reload"]
