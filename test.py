from iota import *
import subprocess
import urllib
import json

IP = "http://163.225.223.80:14265"
api = Iota(IP, "EDCEMKUNKEBDQIFBTAXV9TL9IWXGVURHVHDNCOKVBZNUNSGLCWTERZHYNFOGKYFHXTFL9OJTCIWVGEOX")
"""
command = {
    "command": "Snapshot.getState"
}

stringified = json.dumps(command)

headers = {
    "content-type" : "application/json",
    "X-IOTA-API-Version" : "1"
}
request = urllib.request.Request(url = IP, data = stringified.encode("utf-8"), headers = headers)
returnData = urllib.request.urlopen(request).read()
jsonData = json.loads(returnData)
print(type(jsonData))

#############
command = {
    "command" : "findTransactions",
    "addresses": ["ORATHOJMW9KDYQQDPBPUZJBEFTEQWTIJNIDDOWXJQFKSLEKMPHOAWDHKROUFXOWXMNBJRZPDKBTSSGTPW"]
}
stringified = json.dumps(command)

headers = {
    "content-type" : "application/json",
    "X-IOTA-API-Version" : "1"
}

request = urllib.request.Request(url = IP, data = stringified.encode("utf-8"), headers = headers)
returnData = urllib.request.urlopen(request).read()

jsonData = json.loads(returnData)
print(jsonData)

"""
####
command = {
    "command" : "getTrytes",
    #"hashes" : jsonData["hashes"]
    "hashes" : ["UJOAY9MHONDN9EDGGQDOX9ZBZJDTMWLNLLLESUWYAHU9KJFVTHEL9ZXAEGHMCCWNWQWRGMRXOKRG99999"]
}

stringified = json.dumps(command)

headers = {
    "content-type" : "application/json",
    "X-IOTA-API-Version" : "1"
}

request = urllib.request.Request(url = IP, data = stringified.encode("utf-8"), headers = headers)
returnData = urllib.request.urlopen(request).read()

jsonData = json.loads(returnData)

print(len(jsonData["trytes"]))
txn_1 = Transaction.from_tryte_string(jsonData["trytes"][0].encode("utf-8"))

#print(TryteString(txn_1.tag).decode())
#print(str(txn_1.bundle_hash))
print(txn_1.tag)
"""
##############
command = {
    'command': 'findTransactions',
    'bundles': [str(txn_1.bundle_hash)]
}

stringified = json.dumps(command)

headers = {
    'content-type': 'application/json',
    'X-IOTA-API-Version': '1'
}

request = urllib.request.Request(url=IP, data=stringified.encode("utf-8"), headers=headers)
returnData = urllib.request.urlopen(request).read()

jsonData = json.loads(returnData)


###############
command = {
    "command" : "getTrytes",
    "hashes" : jsonData["hashes"]
}

stringified = json.dumps(command)

headers = {
    "content-type" : "application/json",
    "X-IOTA-API-Version" : "1"
}

request = urllib.request.Request(url = IP, data = stringified.encode("utf-8"), headers = headers)
returnData = urllib.request.urlopen(request).read()

jsonData = json.loads(returnData)

print(len(jsonData["trytes"]))
txn_1 = Transaction.from_tryte_string(jsonData["trytes"][1].encode("utf-8"))

print(txn_1.signature_message_fragment.as_string())
"""
