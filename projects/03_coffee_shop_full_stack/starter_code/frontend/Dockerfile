FROM node:12.20.1-alpine
RUN apk update && apk upgrade
RUN apk add curl
RUN addgroup -S nodeuser && adduser -S nodeuser -G nodeuser
WORKDIR /frontend
COPY . .
RUN chown -R nodeuser:nodeuser /frontend
RUN chmod 755 /frontend
USER nodeuser
RUN npm install
ENTRYPOINT ["npm", "start"]