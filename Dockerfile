FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip config set global.index-url https://pypi-mirror.gitverse.ru/simple/ && \
    pip config set global.trusted-host pypi-mirror.gitverse.ru && \
    pip config set global.timeout 300 && \
    pip config set global.retries 10

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

    
COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "credit_bank.wsgi:application", "--bind", "0.0.0.0:8000"]