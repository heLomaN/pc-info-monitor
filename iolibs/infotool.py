import requests
import json


def get_public_ip():
    try:
        url = "http://ip.42.pl/raw"

        request = requests.get(url).text
        # theIP = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}",request)
        return request
    except Exception as e:
        return ""