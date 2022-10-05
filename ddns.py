import re
import json
from os import environ
from urllib.request import urlopen, Request


zone = environ.get("CF_ZONE")      # domain.tld
record = environ.get("CF_RECORD")  # sub.domain.tld
token = environ.get("CF_TOKEN")    # https://dash.cloudflare.com/profile/api-tokens - Get a TOKEN not a KEY


endpoint = "https://api.cloudflare.com/client/v4/zones"
headers = {"Authorization": f"Bearer {token}"}


def get_ip():
    """
    get the ip address of whoever executes the script
    """
    req = Request("https://1.1.1.1/cdn-cgi/trace")
    res = urlopen(req).read().decode()

    return re.search(r"ip=(\d.+)", res).group(1)


def get_zone_id():
    """
    get the domain (zone) id
    https://api.cloudflare.com/#zone-list-zones
    """
    req = Request(url=f"{endpoint}?name={zone}",
                  headers=headers,
                  )
    res = json.loads(urlopen(req).read())["result"]

    if len(res) == 0:
        raise ValueError("Invalid CF_ZONE")

    return res[0]["id"]


def get_record_data(zone_id):
    """
    get the record (sub domain) id
    https://api.cloudflare.com/#dns-records-for-a-zone-list-dns-records
    """
    req = Request(url=f"{endpoint}/{zone_id}/dns_records?name={record}",
                  headers=headers,
                  )
    res = json.loads(urlopen(req).read())["result"]

    if len(res) == 0:
        raise ValueError("Invalid CF_RECORD")
    elif res[0]["type"] != 'A':
        # Can only update record type A
        raise ValueError("Record is not type A")

    return [res[0]["id"], res[0]["content"]]


def update_record(content, zone_id, record_id):
    """
    update the record
    https://api.cloudflare.com/#dns-records-for-a-zone-patch-dns-record
    """
    req = Request(url=f"{endpoint}/{zone_id}/dns_records/{record_id}",
                  data=json.dumps({"content": content}).encode(),
                  headers=headers,
                  method="PATCH",
                  )
    res = json.loads(urlopen(req).read())

    return [res["success"], res["errors"], res["messages"]]


def main():
    if None in (zone, record, token):
        raise ValueError("Missing environment variables")

    zone_id = get_zone_id()
    print(f"Zone ID: {zone_id}")

    record_id, record_ip = get_record_data(zone_id)
    print(f"Record ID: {record_id}")
    print(f"Record IP: {record_ip}")

    current_ip = get_ip()
    print(f"Current IP: {current_ip}")

    if current_ip == record_ip:
        print("Dont need to update")
        return

    success, error, messages = update_record(current_ip, zone_id, record_id)

    if success:
        print("Success")
    else:
        print(f"Errors:", error)
        print(f"Messages:", messages)


if __name__ == "__main__":
    main()
