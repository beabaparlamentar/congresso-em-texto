FROM python:3.11

# Upgrading packages and installing PIP
RUN apt-get update -y && \
    apt-get install -y python3-pip

WORKDIR /app

COPY . .

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["poetry", "run", "python", "main.py"]
