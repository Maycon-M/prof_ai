# Stage de build para compilar as dependências
FROM python:3.12.11-alpine3.22 AS build

WORKDIR /app

RUN apk update && apk add --no-cache \
      postgresql-dev \
      build-base \
      musl-dev \
      python3-dev

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage final mais enxuto
FROM python:3.12.11-alpine3.22

WORKDIR /app

# Somente runtime
RUN apk update && apk add --no-cache \
      postgresql-libs

COPY --from=build /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=build /usr/local/bin/ /usr/local/bin/

COPY . /app

EXPOSE 8888

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "src.main.server.server:app", "--bind", "0.0.0.0:8888"]


# CMD ["uvicorn", "src.main.server.server:app", "--reload", "--host", "0.0.0.0", "--port", "8888"]

# docker build -t api_prof_ai -f docker/Dockerfile .
# docker run -d -p 8888:8888 --env-file .env --name api_prof_ai_container api_prof_ai