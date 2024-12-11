"""Flask Echo IP"""

__version__ = "2.0.0"

import os

from http import HTTPStatus

from flask import Flask, request

app = Flask(__name__)

FORWARDED_IP_HEADER_NAME = os.environ.get(
    "FORWARDED_IP_HEADER_NAME",
    "X-Forwarded-For"
)

def get_ip() -> str | None:
    return request.headers.get(FORWARDED_IP_HEADER_NAME)

def do_502():
    code = HTTPStatus.BAD_GATEWAY
    body = f"Gateway didn't provide {FORWARDED_IP_HEADER_NAME}\n"

    return body, code

def do_200(ip: str):
    return f"{ip}\n"

@app.route("/")
def index():
    if (ip := get_ip()) is None:
        return do_502()
    return do_200(ip)
