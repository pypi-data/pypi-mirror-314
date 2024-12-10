#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import volkanic

cmddef = """
l               joker.superuser.cli.locators:main
sha1b32         joker.superuser.cli.chksums:sha1b32
sha384b64       joker.superuser.cli.chksums:sha384b64
chksum-rename   joker.superuser.cli.chksums:main
uuid            joker.superuser.cli.uuidgen:main
pydir           joker.superuser.tools.pydir
pyentry         joker.superuser.tools.pyentry
unsource        joker.superuser.tools.unsource
cases           joker.superuser.tools.cases
dup             joker.superuser.tools.dedup
setop           joker.superuser.tools.setop
rmdir           joker.superuser.tools.remove
apt             joker.superuser.tools.apt
url             joker.superuser.tools.urls
urls            joker.superuser.tools.urls:runloop
urlquote        joker.superuser.tools.urls:urlquote
htmlesc         joker.superuser.tools.urls:htmlescape
"""

_prog = "python3 -m joker.superuser"
registry = volkanic.CommandRegistry.from_cmddef(cmddef, _prog)

if __name__ == "__main__":
    registry()
