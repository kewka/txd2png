FROM ubuntu:16.04

WORKDIR /usr/src/app

COPY . .

# Build rwtools
RUN apt-get update \
    && apt-get install make build-essential libpng-dev -y \
    && ./build

# Install python 3
RUN apt-get install -y python3-pip python3-dev

CMD ["python3", "server.py"]