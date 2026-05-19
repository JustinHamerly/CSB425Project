FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir requests pandas pyarrow
COPY jobs/ /app/jobs/