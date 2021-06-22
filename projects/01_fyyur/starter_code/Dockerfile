FROM python:3.9.0-alpine3.12

RUN apk update && apk upgrade
RUN apk add --no-cache python3-dev g++ gcc gpgme-dev libc-dev musl-dev nodejs npm

RUN addgroup --system pythonuser -g 1001
RUN adduser --system -g pythonuser --uid 1001 pythonuser

WORKDIR /fyyur

COPY requirements.txt .

RUN chown -R pythonuser:pythonuser /fyyur
RUN chmod 755 /fyyur

USER 1001

RUN python -m pip install -r /fyyur/requirements.txt

ENTRYPOINT ["python", "app.py"]
