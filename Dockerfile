FROM python:3.12-slim
RUN apt-get update -qq && apt-get install -y -qq git >/dev/null && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
CMD ["./repro.sh"]
