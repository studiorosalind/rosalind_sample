FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --production=false

COPY . .

RUN npm run build

EXPOSE 3000

ENV PATH /app/node_modules/.bin:$PATH

CMD ["npm", "run", "start"]
