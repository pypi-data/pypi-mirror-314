#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import argparse
from uuid import UUID, uuid1, uuid4


def _format(uuidobj: UUID, std=False, lower=False) -> str:
    if std:
        s = str(uuidobj)
    else:
        s = uuidobj.bytes.hex()
    if not lower:
        s = s.upper()
    return s


def main(prog=None, args=None):
    desc = "generate uuid"
    parser = argparse.ArgumentParser(prog=prog, description=desc)
    add = parser.add_argument
    add("-l", "--lower", action="store_true", help="lower case")
    add("-s", "--std", action="store_true", help="use standard hyphen-delimited format")
    add("-v", "--ver", type=int, default=4, choices=[1, 4])

    ns = parser.parse_args(args)
    versions = {1: uuid1, 4: uuid4}
    func = versions[ns.ver]
    print(_format(func(), ns.std, ns.lower))
