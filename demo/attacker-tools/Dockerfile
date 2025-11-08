FROM python:3.13-slim

# for templating
RUN apt-get update && apt-get install -y gettext-base && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY templates/ templates/
COPY app.py .

EXPOSE 8080

CMD ["/bin/sh", "-c", "envsubst < templates/index.template.html > templates/index.html && python app.py"]
