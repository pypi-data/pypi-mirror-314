#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import os
import subprocess
import sys
import pathlib


def main(_prog, args):
    proc = subprocess.run(["hostname"], capture_output=True)
    hostname = proc.stdout.decode("utf-8").strip()
    username = os.environ.get("USER", "user")
    for path in args:
        path = pathlib.Path(path).absolute()
        print(f"{username}@{hostname}:{path}")
        print(path.as_uri())


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
