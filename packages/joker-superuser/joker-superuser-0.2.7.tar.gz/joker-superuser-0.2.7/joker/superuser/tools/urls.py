#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import argparse
import shlex
import sys
from html import escape
from urllib.parse import quote_plus

import pyperclip
from joker.superuser.environ import JokerInterface
from joker.textmanip.url import url_simplify
from volkanic.utils import ignore_arguments

ji = JokerInterface()


def urlquote(_prog: str, args):
    for s in args:
        print(quote_plus(s))


def htmlescape(_prog: str, args):
    for s in args:
        print(escape(s))


def smart_url_simplify(url, queries):
    config = ji.conf["urls"]
    for pattern, _queries in config.items():
        if pattern in url:
            queries = _queries
            break
    return str(url_simplify(url, queries))


def _copy_and_print(url: str):
    print(url)
    print(shlex.quote(url))
    pyperclip.copy(url)


def run(prog, args):
    desc = "simplify a url"
    parser = argparse.ArgumentParser(prog=prog, description=desc)
    parser.add_argument("url")
    parser.add_argument("query", nargs="*")
    ns = parser.parse_args(args)
    url = str(smart_url_simplify(ns.url, ns.query))
    _copy_and_print(url)


@ignore_arguments
def runloop():
    while True:
        userinput = input("URL> ")
        parts = shlex.split(userinput)
        if not parts:
            continue
        url = parts[0]
        queries = parts[1:]
        try:
            url = smart_url_simplify(url, queries)
        except Exception as e:
            print(e.__class__.__name__, e, file=sys.stderr)
            continue
        _copy_and_print(url)
