FROM python:3.11-slim-bullseye

# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends gcc python3-dev git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

# create a venv.
RUN python3 -m venv /opt/venv --upgrade-deps

# Make sure we use the venv.
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV="/opt/venv"

RUN pip3 install --no-cache-dir .[wsgi]

CMD ["./entrypoint.sh"]
