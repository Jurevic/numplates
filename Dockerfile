FROM python:3.6.8-alpine3.9

# Set workdir
WORKDIR /usr/src/app

# Load requirements
COPY /requirements.txt /requirements.txt

# Install build deps
RUN set -ex \
    && apk update \
    && apk add \
        gcc \
        jpeg-dev \
        make \
        libc-dev \
        openssl-dev \
        zlib-dev

# Install python requirements
RUN python3 -m venv /venv \
    && /venv/bin/pip install -U pip \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/venv/bin/pip install --no-cache-dir -r /requirements.txt"

# Load source
COPY . .

# Execute
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["serve"]

# Listen on
EXPOSE 8000