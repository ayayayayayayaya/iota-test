#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

with open("snapshot.json") as f:
    snapshot = json.load(f)

snapshot["ixi"]["state"].keys()
#↑これがアドレス全部
