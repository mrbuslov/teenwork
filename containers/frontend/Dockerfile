FROM node:14 AS development
ENV NODE_ENV development
WORKDIR /app

COPY ./frontend/package.json ./
COPY ./frontend ./

CMD ["npm", "run", "docker_start"]
