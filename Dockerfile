FROM python:3.9-slim-bullseye

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
