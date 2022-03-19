# Cloudflare record update

A small python script that updates a cloudflare dns record with your current ip.

You need load the `.env` in memory before runs the `ddns.py`. The necessary values are inside `.env.sample`.

You can register a cronjob to execute in an interval of choice.

## docker-compose

You can simple run `docker compose up` if the envrionment variables are defined.

The cron schedule is defined in [compose's entrypoint](https://github.com/fabricionaweb/cloudflare-ddns-python/blob/master/compose.yaml#L26), if you want change the time to run.
