# Python

Small script to update Cloudflare DNS record with your current ip (Dynamic DNS).

- you need load the `.env` in memory before runs the `ddns.py` (or hard code the values)
- you can register a cronjob to execute in an interval of choice

# OpenWrt

Bash script to run on OpenWrt without dependencies (just cURL) to use with [Hotplug](https://openwrt.org/docs/guide-user/base-system/hotplug):

- copy the file [25-ddns](./25-ddns) to `/etc/hotplug.d/iface/25-ddns`
- copy the file [ddns.sh](./25-ddns) to `/root/ddns.sh`
  - change to your values

Everytime WAN interface changes the ip the script will be called.

To check the logs use `logread -f -e hotplug`
