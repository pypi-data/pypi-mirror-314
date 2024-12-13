"""
A place to register plugin hooks
"""
from conda import plugins
import os
from urllib.parse import urlparse  

def extract_host(url):  
    parsed_url = urlparse(url)  
    return parsed_url.hostname  


@plugins.hookimpl
def conda_session_headers(host: str):
    quetz_host = os.environ.get("QUETZ_HOST", None)
    if quetz_host:
        quetz_host = extract_host(quetz_host)

    quetz_api_key = os.environ.get("QUETZ_API_KEY", None)
    if quetz_host and quetz_api_key:
        if quetz_host.lower() in host.lower():
            yield plugins.CondaRequestHeader(
                name="X-API-Key",
                value=quetz_api_key,
            )