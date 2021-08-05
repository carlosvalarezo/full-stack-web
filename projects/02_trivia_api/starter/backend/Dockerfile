FROM python:3.8-slim-buster

RUN apt update -y && apt upgrade -y
RUN apt-get install -y postgresql-client
RUN useradd --user-group --system --create-home --no-log-init pythonuser

WORKDIR /backend

COPY requirements.txt .

RUN chown -R pythonuser:pythonuser /backend
RUN chmod 755 /backend

USER pythonuser

RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "flaskr/app.py", "-h", "0.0.0.0"]
