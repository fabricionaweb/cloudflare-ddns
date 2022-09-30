# Python

Small script to update Cloudflare DNS record with your current ip (Dynamic DNS).

- you need load the `.env` in memory before runs the `ddns.py` (or hard code the values)
- you can register a cronjob to execute in an interval of choice

# OpenWrt

Bash script to run on OpenWrt without dependencies (just cURL) to use with [Hotplug](https://openwrt.org/docs/guide-user/base-system/hotplug):

- copy the file [90-ddns](./90-ddns) to `/etc/hotplug.d/iface/90-ddns`
  - change to your values

Everytime WAN interface changes the ip the script will be called.

To check the logs use `logread -e hotplug`
