FROM node:lts

RUN npm install -g @biomejs/biome

WORKDIR /workspace/app

COPY ./package.json ./

RUN npm install
RUN npx playwright install --with-deps

COPY ./src ./src
COPY ./public ./public
COPY ./next.config.ts .
COPY ./tsconfig.json .

CMD ["npm", "run", "dev"]