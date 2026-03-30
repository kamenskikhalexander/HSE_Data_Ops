FROM python:3.11-slim

WORKDIR /ml-service

RUN pip install --no-cache-dir fastapi uvicorn scikit-learn sqlalchemy psycopg2-binary

COPY app.py /ml-service/app.py

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
