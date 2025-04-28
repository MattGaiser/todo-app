FROM python:3.11

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary pydantic
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
