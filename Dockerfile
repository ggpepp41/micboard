FROM python:3

LABEL org.opencontainers.image.source=https://github.com/ggpepp41/micboard

WORKDIR /usr/src/app
EXPOSE 8058
CMD ["python3", "py/micboard.py"]

RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install nodejs


COPY package.json .

RUN npm install --omit=dev

COPY /py/requirements.txt /usr/src/app/py/requirements.txt
RUN pip3 install -r py/requirements.txt

COPY . .
RUN npm run build


