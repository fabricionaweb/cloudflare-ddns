# Cloudflare record update

A small python script that updates a cloudflare dns record with your current ip.

You need load the `.env` in memory before runs the `ddns.py`. The necessary values are inside `.env.sample`.

You can register a cronjob to execute in an interval of choice.

## docker

A tiny alpine image are builded with only the script inside. You only need to set the correct environment variables like in `.env.sample`

`docker run --init --rm --env-file=.env ghcr.io/fabricionaweb/cloudflare-ddns`

## docker-compose

You can simple run `docker compose up` if the environment variables are defined.
