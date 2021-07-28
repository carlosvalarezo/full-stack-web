FROM node:16.0.0-buster-slim

RUN apt update -y && apt upgrade -y
RUN useradd --user-group --system --create-home --no-log-init nodeuser

WORKDIR /frontend

COPY package.json .

RUN chown -R nodeuser:nodeuser /frontend
RUN chmod 755 /frontend

USER nodeuser

RUN npm install

ENTRYPOINT ["npm", "start"]
