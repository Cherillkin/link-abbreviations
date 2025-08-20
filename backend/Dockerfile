FROM python:3.11-alpine

RUN apk add --no-cache postgresql-client gcc musl-dev python3-dev libffi-dev

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

WORKDIR /app

CMD ["uvicorn", "cmd.main:app", "--host", "0.0.0.0", "--port", "8000"]
