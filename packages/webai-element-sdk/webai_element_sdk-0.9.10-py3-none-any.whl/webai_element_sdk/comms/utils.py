import json
import os
import socket
from functools import cache

CONFIG_PATH: str = os.getenv("CONFIG_PATH")


@cache
def load_config(key: int):
    """Load element configuration"""
    with open(CONFIG_PATH, "r") as file:
        return json.load(file)


def get_default_gateway():
    """Obtain the ip address of agent outside of container"""
    try:
        return socket.gethostbyname("host.docker.internal")
    except socket.gaierror:
        with open("/proc/net/route") as f:
            for line in f.readlines():
                fields = line.strip().split()
                # Check for default gateway (destination 0.0.0.0)
                if fields[1] != "00000000":
                    continue
                gateway_hex = fields[2]
                # Convert hexadecimal gateway to decimal IP
                gateway_ip = [
                    str(int(gateway_hex[i : i + 2], 16)) for i in [6, 4, 2, 0]
                ]
                return ".".join(gateway_ip)
    return "localhost"


class MaxRetriesExceededError(Exception):
    """Raised when the maximum number of retries is exceeded."""


async def async_noop(*args) -> None:
    pass


def noop(*args) -> None:
    pass
