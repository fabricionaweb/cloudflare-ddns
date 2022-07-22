#!/bin/sh

# ---
# settings
ZONE="domain.com"
RECORD="sub.domain.com"
# you need to generate the API Token on dashboard
# https://api.cloudflare.com/#getting-started-requests
TOKEN=""

# ---
# cloudflare api
ENDPOINT="https://api.cloudflare.com/client/v4"

# ---
# gets the ip from WAN
# https://openwrt.org/docs/guide-developer/network-scripting#get_wan_address
. /lib/functions/network.sh
network_flush_cache
network_find_wan NET_IF
network_get_ipaddr NET_ADDR "${NET_IF}"
echo "Current IP: ${NET_ADDR}"

# ---
# gets the domain zone id
# https://api.cloudflare.com/#zone-list-zones
ZONE_ID=$(curl -s -X GET "${ENDPOINT}/zones?name=${ZONE}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jsonfilter -e "@.result[0].id")
echo "Zone ID: ${ZONE_ID}"

# ---
# gets the dns record id
# https://api.cloudflare.com/#dns-records-for-a-zone-list-dns-records
RECORD_ID=$(curl -s -X GET "${ENDPOINT}/zones/${ZONE_ID}/dns_records?name=${RECORD}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jsonfilter -e "@.result[0].id")
echo "Record ID: ${RECORD_ID}"

# ---
# updates the dns record
# https://api.cloudflare.com/#dns-records-for-a-zone-patch-dns-record
RESULT=$(curl -s -X PATCH "${ENDPOINT}/zones/${ZONE_ID}/dns_records/${RECORD_ID}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  --data "{\"content\":\"${NET_ADDR}\"}" | jsonfilter -e "@['success','errors','messages']")

echo "Result: ${RESULT}"
