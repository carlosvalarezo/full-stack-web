FROM python:3.6-alpine

RUN apk update && apk upgrade
RUN apk add --no-cache postgresql-libs postgresql-dev
RUN apk add --virtual .build-deps python3-dev g++ gcc gpgme-dev libc-dev musl-dev curl nodejs npm


RUN addgroup --system pythonuser -g 1001
RUN adduser --system -g pythonuser --uid 1001 pythonuser

WORKDIR /fyyur

COPY requirements.txt .

RUN chown -R pythonuser:pythonuser /fyyur
RUN chmod 755 /fyyur

USER 1001

RUN python -m pip install -r /fyyur/requirements.txt

RUN npm install bootstrap@3

EXPOSE 5000

ENTRYPOINT ["python", "app.py", "-h", "0.0.0.0"]
