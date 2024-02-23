# -*- coding: utf-8 -*-

import hashlib


def create_uuid(url, encoding='utf-8'):
    return hashlib.md5(url.encode(encoding)).hexdigest()
