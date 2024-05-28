FROM python:3.9-slim-bullseye

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip3 install --no-cache-dir .

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "sdx_lc"]
