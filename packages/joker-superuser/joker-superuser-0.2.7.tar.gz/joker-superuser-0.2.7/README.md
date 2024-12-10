joker-superuser
===============

Commandline utilities
---------------------

Generate UUID:

    $ sus uuid
    8EDFF28CB26A4C13BF8D4AD8BDC5434A

    $ sus uuid -s
    FC8A0CC5-63BE-459A-8E86-AD8A1A87A767

    $ sus uuid -sl
    836a9b1f-a5ac-418d-9cce-1b06f3ac24e6

Compute Base32 encoded SHA1 checksums:

    sus sha1b32 example.txt
    find . -type f -exec sus sha1b32 {} \;

Compute Base64 encoded SHA384 checksums:

    sus sha384b64 example.txt
    find . -type f -exec sus sha384b64 {} \;

Miscellaneous
-------------

Get resources with SVN:

    svn export https://github.com/frozflame/joker-superuser/trunk/resources sus-resources

Get resources with curl and tar:

    mkdir sus-resources
    curl -L "https://github.com/frozflame/joker-superuser/archive/master.tar.gz" | tar xz -C sus-resources --strip-components 2 joker-superuser-master/resources/ 

Recent changes
--------------

version 0.2.5

- add sub-commands `l` (locators) and `chksumdir`
- require Python version 3.6+