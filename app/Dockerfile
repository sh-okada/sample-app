FROM node:lts

RUN npm install -g @biomejs/biome

WORKDIR /workspace/app

COPY ./package.json ./
COPY ./package-lock.json ./

RUN npm install

COPY ./src ./src
COPY ./public ./public
COPY ./next.config.ts .
COPY ./tsconfig.json .

CMD ["npm", "run", "dev"]