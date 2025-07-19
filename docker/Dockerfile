FROM python:3.12.11-alpine3.22

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
        curl \
        apt-transport-https \
        gnupg \
        unixodbc \
        unixodbc-dev

RUN apt-get remove -y unixodbc-common odbcinst libodbc2 libodbcinst2 || true

RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/keyrings/microsoft.asc > /dev/null && \
    echo "deb [signed-by=/etc/apt/keyrings/microsoft.asc] https://packages.microsoft.com/debian/11/prod bullseye main" | tee /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update && ACCEPT_EULA=Y apt-get install -y \
        msodbcsql18 \
        --allow-downgrades --allow-remove-essential --allow-change-held-packages \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8888

CMD ["gunicorn","-k","uvicorn.workers.UvicornWorker",  "src.main.server.server:app", "--bind", "0.0.0.0:8888"]

# CMD ["uvicorn", "src.main.server.server:app", "--reload", "--host", "0.0.0.0", "--port", "8888"]

# docker build -t api_prof_ai -f docker/Dockerfile .
# docker run -d -p 8888:8888 --env-file .env --name api_prof_ai_container api_prof_ai