#/usr/bin/env/python
## -*- coding: utf-8 -*-

import subprocess
import glob
import os
import getpass

snapshot = "/home/{}/git/iri/target/Snapshot.txt".format(getpass.getuser())
tx_dir = "/home/{}/git/iri/target/export/".format(getpass.getuser())

filepath = glob.glob(tx_dir + "*")
for fp in filepath:
    if not os.path.isdir(fp):
        with open(fp) as f:
            lines = f.readlines()
        data = lines[0].replace("\n","") + "\;0"
        subprocess.call("echo {} >> {}".format(data, snapshot), shell=True)
