ARG ARCH=
FROM ${ARCH}python:alpine

# https://crontab.guru/every-15-minutes
ENV CRON_TIME "*/15 * * * *"
COPY ddns.py /

ENTRYPOINT /bin/sh -c "echo '$CRON_TIME python /ddns.py' | crontab - && crond -fd8"
