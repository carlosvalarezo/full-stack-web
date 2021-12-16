FROM python:3.8-slim-buster

RUN apt-get update -y \
    && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install cryptography
RUN useradd --user-group --system --create-home --no-log-init pythonuser

WORKDIR /backend

COPY requirements.txt .

RUN chown -R pythonuser:pythonuser /backend
RUN chmod 755 /backend

USER pythonuser

RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "src/api.py", "-h", "0.0.0.0"]
