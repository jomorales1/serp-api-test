FROM python:3.9-alpine

RUN apk update
RUN apk add build-base
RUN apk add musl-dev
RUN apk add linux-headers
RUN apk add py3-pip
RUN apk add libpq-dev
RUN apk add cmake
RUN apk add pkgconfig
RUN apk add --no-cache bash

COPY . ./serp-api-test/
WORKDIR /serp-api-test/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN apk add curl
RUN apk add nano

EXPOSE 80

# CMD ["uvicorn", "main:app", "--root-path", "/serp", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
