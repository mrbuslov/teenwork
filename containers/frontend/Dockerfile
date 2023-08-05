FROM node:17.4.0
WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY ./frontend/package.json ./
COPY ./frontend/package-lock.json ./
RUN npm install --silent
# install 4.0.3, because this version watch the changes and reloads the server in docker
RUN npm install react-scripts@4.0.3 -g --silent

COPY ./frontend ./

CMD ["npm", "start"]