import pathlib
import subprocess
import time

import requests
from connect_test import config


class Compose(object):
    """Manages docker-compose for tests"""
    def __init__(self):
        self.working_dir = pathlib.Path(__file__).resolve().parent.parent

    def up(self):
        subprocess.run(["docker-compose", "up", "--detach", "--remove-orphans"], cwd=self.working_dir)
        time.sleep(5)
        start = time.monotonic()
        while start + 60 > time.monotonic():
            resp = requests.get(config.NGINX_URL)
            if resp.status_code == 200:
                return config.CONNECT_REST_URL
            time.sleep(2)
        raise RuntimeError("Connect not available")

    def down(self):
        subprocess.run(["docker-compose", "down", "--rmi", "local", "--remove-orphans"], cwd=self.working_dir)
