#/usr/bin/env python
# -*- coding: utf-8 -*-

from iota import *
import urllib
import json

class getTransaction:
    def __init__(self, args):
        self.host_ip = args.host_ip
        self.bundle_hash = []

    def getSnapshot(self):
        command = {
            "command": "Snapshot.getState"
        }

        stringified = json.dumps(command)

        headers = {
            "content-type" : "application/json",
            "X-IOTA-API-Version" : "1"
        }
        request = urllib.request.Request(url = self.host_ip, data = stringified.encode("utf-8"), headers = headers)
        returnData = urllib.request.urlopen(request).read()
        addresses = json.loads(returnData)
        return addresses

    def getHashes(self, addresses):
        command = {
            "command" : "findTransactions",
            "bundles": [addresses]
        }
        stringified = json.dumps(command)

        headers = {
            "content-type" : "application/json",
            "X-IOTA-API-Version" : "1"
        }

        request = urllib.request.Request(url = self.host_ip, data = stringified.encode("utf-8"), headers = headers)
        returnData = urllib.request.urlopen(request).read()
        hashes = json.loads(returnData)
        return self.getTrytes(hashes)

    def getTrytes(self, hashes):
        txn = []
        if type(hashes) == dict:
            command = {
                "command" : "getTrytes",
                "hashes" : hashes["hashes"]
            }
        elif type(hashes) == str:
            command = {
                "command" : "getTrytes",
                "hashes" : [hashes]
            }

        stringified = json.dumps(command)

        headers = {
            "content-type" : "application/json",
            "X-IOTA-API-Version" : "1"
        }

        request = urllib.request.Request(url = self.host_ip, data = stringified.encode("utf-8"), headers = headers)
        returnData = urllib.request.urlopen(request).read()
        jsonData = json.loads(returnData)
        for dat in jsonData["trytes"]:
            txn.append(Transaction.from_tryte_string(dat.encode("utf-8")))
        return self.findTransactions(txn)

    def findTransactions(self, txn):
        for bh in txn:
            if bh.bundle_hash not in self.bundle_hash:
                self.bundle_hash.append(str(bh.bundle_hash))

        command = {
            'command': 'findTransactions',
            'bundles': self.bundle_hash
        }

        stringified = json.dumps(command)

        headers = {
            'content-type': 'application/json',
            'X-IOTA-API-Version': '1'
        }

        request = urllib.request.Request(url=self.host_ip, data=stringified.encode("utf-8"), headers=headers)
        returnData = urllib.request.urlopen(request).read()
        hashes = json.loads(returnData)

        txn_bundle = self.getTransactions(hashes)
        return txn, txn_bundle

    def getTransactions(self, hashes):
        txn = []
        command = {
            "command" : "getTrytes",
            "hashes" : hashes["hashes"]
        }

        stringified = json.dumps(command)

        headers = {
            "content-type" : "application/json",
            "X-IOTA-API-Version" : "1"
        }

        request = urllib.request.Request(url = self.host_ip, data = stringified.encode("utf-8"), headers = headers)
        returnData = urllib.request.urlopen(request).read()

        jsonData = json.loads(returnData)
        for dat in jsonData["trytes"]:
            txn.append( Transaction.from_tryte_string(dat.encode("utf-8")))
        return txn
