#/usr/bin/env python
# -*- coding: utf-8 -*-

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import subprocess
import time
import getpass
import os

snapshot = "/home/{}/git/iri/target/Snapshot.txt".format(getpass.getuser())
tx_dir = "/home/{}/git/iri/target/export/".format(getpass.getuser())


class ChangeHandler(FileSystemEventHandler):
    def on_creted(self, event):
        print("created")
        filepath = event.src_path
        filename = os.path.basename(filepath)
        if not os.path.isdir(filepath):
            print(filename)
            with open(filepath) as f:
                lines = f.readlines()
            data = lines[0].replace("\n","") + "\;0"
            subprocess.call("echo {} >> {}".format(data, snapshot), shell=True)
            
    def on_moved(self, event):
        print("moved")
        filepath = event.src_path
        filename = os.path.basename(filepath)
        if not os.path.isdir(filepath):
            print(filename)
            with open(filepath) as f:
                lines = f.readlines()
            data = lines[0].replace("\n","") + "\;0"
            subprocess.call("echo {} >> {}".format(data, snapshot), shell=True)

    def on_modified(self, event):
        print("modified")
        filepath = event.src_path
        time.sleep(1)
        filename = os.path.basename(filepath)
        if not os.path.isdir(filepath):
            print(filename)
            with open(filepath) as f:
                lines = f.readlines()
            data = lines[0].replace("\n","") + "\;0"
            subprocess.call("echo {} >> {}".format(data, snapshot), shell=True)

    def on_deleted(self, event):
        filepath = event.src_path
        print(filepath)

def main():
    while True:
        event_handler = ChangeHandler()
        observer = Observer()
        observer.schedule(event_handler, tx_dir, recursive = True)
        observer.start()
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
