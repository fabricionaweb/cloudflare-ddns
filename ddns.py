import re
import json
from os import environ
from urllib.request import urlopen, Request


domain = environ.get("DOMAIN")
dns = environ.get("DNS")
email = environ.get("API_USER")
token = environ.get("API_KEY")

endpoint = "https://api.cloudflare.com/client/v4/zones"
headers = {"X-Auth-Email": email, "X-Auth-Key": token}


def get_ip():
    """
    get the ip address of whoever executes the script
    """
    req = Request("https://cloudflare.com/cdn-cgi/trace")
    res = urlopen(req).read().decode()

    return re.search(r"ip=(\d.+)", res).group(1)


def get_zone_id():
    """
    get the domain id
    """
    req = Request(url=endpoint, headers=headers)
    res = json.loads(urlopen(req).read())

    for zone in res["result"]:
        if zone["name"] == domain:
            return zone["id"]


def get_record_id(zone_id):
    """
    get the dns id
    """
    req = Request(url=f"{endpoint}/{zone_id}/dns_records", headers=headers)
    res = json.loads(urlopen(req).read())

    for record in res["result"]:
        if record["name"] == dns:
            return record["id"]


def set_ip(current_ip, zone_id, record_id):
    """
    set the ip in via cloudflare api
    """
    req = Request(url=f"{endpoint}/{zone_id}/dns_records/{record_id}",
                  data=json.dumps({"content": current_ip}).encode(),
                  headers=headers,
                  method="PATCH",
                  )
    res = json.loads(urlopen(req).read())

    return [res["success"], res["errors"], res["messages"]]


def main():
    if None in (domain, dns, email, token):
        raise ValueError("Missing environment variables")

    current_ip = get_ip()
    print(f"Current IP: {current_ip}")

    zone_id = get_zone_id()
    print(f"Zone ID: {zone_id}")

    record_id = get_record_id(zone_id)
    print(f"Record ID: {record_id}")

    success, error, messages = set_ip(current_ip, zone_id, record_id)

    if success:
        print("Success")
    else:
        print(f"Errors:", error)
        print(f"Messages:", messages)


if __name__ == "__main__":
    main()
