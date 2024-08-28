FROM python:3.8-alpine
RUN pip install --upgrade pip
RUN apk update && apk add libpq
RUN apk add ca-certificates && update-ca-certificates
# Change TimeZone
RUN apk add --update tzdata
ENV TZ=America/Sao_Paulo
# Clean APK cache
RUN rm -rf /var/cache/apk/*
RUN apk add --virtual .build-dependencies \ 
            --no-cache \
            python3-dev \
            musl-dev \
            build-base \
            linux-headers \
            pcre-dev \
            gcc \
            postgresql-dev \
	        libffi-dev
RUN apk add --no-cache pcre
WORKDIR /app
#ADD ./requirements.txt /app
ADD ./version.txt /app
#RUN pip install --no-cache-dir --requirement /app/requirements.txt
RUN pip install --no-cache-dir --requirement /app/version.txt
RUN sed -i -e 's/http:/https:/' /etc/apk/repositories
RUN apk del .build-dependencies && rm -rf /var/cache/apk/*
COPY ./ /app
CMD ["uwsgi", "--ini", "wsgi.ini"]


