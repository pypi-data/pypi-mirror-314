#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import json
import subprocess

from joker.superuser.utils import parse_blank_line_separated_records


def lspci():
    proc = subprocess.run(["lspci", "-vmm"], capture_output=True)
    lines = proc.stdout.decode("utf8").splitlines()
    return list(parse_blank_line_separated_records(lines))


def ip_addr():
    cmd = ["ip", "--json", "addr", "show"]
    proc = subprocess.run(cmd, capture_output=True)
    return json.loads(proc.stdout.decode("utf8"))


def get_cpuinfo() -> list[dict[str, str | list]]:
    records = list(parse_blank_line_separated_records(open("/proc/cpuinfo")))
    for record in records:
        record["flags"] = record["flags"].split()
    return records


def get_cpu_model_name() -> str:
    return get_cpuinfo()[0]["model name"]


def get_cpu_flags() -> list[str]:
    return get_cpuinfo()[0]["flags"]
