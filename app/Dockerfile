FROM node:lts


RUN apt-get update && apt-get install -y \
    libgtk2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    libnotify-dev \
    libnss3 \
    libxss1 \
    libasound2 \
    libxtst6 \
    xauth \
    xvfb




RUN npm install -g @biomejs/biome

WORKDIR /workspace/app

COPY ./package.json ./

RUN npm install

COPY ./src ./src
COPY ./public ./public
COPY ./next.config.ts .
COPY ./tsconfig.json .

CMD ["npm", "run", "dev"]