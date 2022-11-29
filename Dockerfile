FROM ubuntu:22.04
WORKDIR /app
COPY . /app
RUN apt update -y && apt upgrade
# Maybe needs to install python3-psycopg2?
RUN apt install -y python3
CMD /app/src/main.py