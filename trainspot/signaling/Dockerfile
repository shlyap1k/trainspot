FROM node:lts

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY ../../../../Desktop/WebRTC-Video-Broadcast-master .

EXPOSE 4000:4000

CMD [ "node", "server.js" ]