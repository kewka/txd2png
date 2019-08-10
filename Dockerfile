FROM ubuntu:16.04

WORKDIR /usr/src/app

COPY . .

# Build rwtools
RUN apt-get update
RUN apt-get install make build-essential libpng-dev -y
RUN ./build

# Install nodejs
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get install -y nodejs

# Install pm2
RUN npm install pm2 -g

CMD ["pm2-runtime", "server.py", "--interpreter=python3"]