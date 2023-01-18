"""
Module which handles with sending of web requests.
"""
import time
import requests

def web_get_url(url):
    """
    Sends HTTP get request to the input url.
    If exception of type HTTPError with response status 429 (which means two many requests) was raised,
    extracts 'Retry-After' from response headers, waits appropriate amount of time
    and resends request again.
    :param url: url
    :type url: str
    :return:
    :rtype:
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response

    except requests.exceptions.HTTPError as errh:
      if errh.response.status_code == 429: # Too Many Requests
        time.sleep(int(errh.response.headers["Retry-After"]))
        response_retry = requests.get(url, timeout=30)
        return response_retry
      else:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
