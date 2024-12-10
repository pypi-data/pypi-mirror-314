#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import argparse
import os

from joker.filesys.utils import b32_sha1sum, b64_sha384sum, spread_by_prefix


def sha1b32(_prog: str, args: list):
    for path in args:
        chksum = b32_sha1sum(path)
        print(chksum, path)


def sha384b64(_prog: str, args: list):
    for path in args:
        chksum = b64_sha384sum(path)
        print(chksum, path)


def chksum_rename(prog: str, args: tuple):
    desc = "rename files based on their checksums"
    parser = argparse.ArgumentParser(prog=prog, description=desc)
    add = parser.add_argument
    add("-t", "--target", default="files", help="output directory")
    add("source", help="input text file")
    ns = parser.parse_args(args)
    target_dir = ns.target
    chksum_file = os.path.abspath(ns.source)
    os.makedirs(target_dir, exist_ok=False)
    for line in open(chksum_file):
        line = line.strip()
        if not line:
            continue
        chksum, old_path = line.split(maxsplit=1)
        if os.path.abspath(old_path) == chksum_file:
            continue
        names = spread_by_prefix(chksum)
        new_path = os.path.join(target_dir, *names)
        print(old_path, "=>", new_path)
        os.renames(old_path, new_path)
