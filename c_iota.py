#/usr/bin/env python
# -*- coding: utf-8 -*-

from iota import *
from getTransaction import getTransaction
import json
import urllib
from op_image import from_tryte_to_picture

class IOTA:
    def __init__(self, args):
        self.api = Iota(args.host_ip, args.seed)
        self.tx = []
        self.args = args
        self.getTransaction = getTransaction(args)
        self.done_approvee_bundle = []
        self.ignore_bundle = [ 'SKBNIFZLLVNPQUUFGAKAHDCCNWPVFZJIEUXWTP9QEEGJDTBHXBIFBGTEFGVLNXJCAD9QLXJIUSXUSUWLC', 'VXBNIWYCR9LYCVJGNAWWYOYUHHLTAODDUKNLJQBSIBCDKWJYB9CESHNLHDPFE99VXEVTJPFKUDPII9JFZ', 'ESN9DHNKFPUWALGLQXXLEFAKLRIWGFGNCVNBQYOGXLNGHQXFKBXGIUBKSHWDHBHNPKYFDWFWVSFIDRSJA']

    def node_info(self):
        #self.node_infomation is type:dict
        self.node_infomation = self.api.get_node_info()
        return self.node_infomation

    def get_bundle(self):
        print(dir(self.api))
        print(self.api.get_bundles())

    def check_index(self):
        if( str(self.node_infomation["latestMilestoneIndex"]) == str(self.node_infomation["latestSolidSubtangleMilestoneIndex"])):
            return True
        else:
            return False

    def set_transaction(self, _address, _message, _tag, _value):
        for adr, msg, tg, val in zip(_address, _message, _tag, _value):
            self.tx.append(ProposedTransaction(
                           address = adr,
                           message = msg,
                           tag = Tag(tg.encode()),
                           value = val))

    def set_bundle(self):
        depth = 20
        bundle = ProposedBundle()
        for transaction in self.tx:
            prev_tx = None
            bundle.add_transaction(transaction)
            approve_hash = self.trunk_and_branch(depth)

            trunk_bundle, trunk_image = self.getTransaction.getTrytes(approve_hash["trunkTransaction"])
            branch_bundle, branch_image = self.getTransaction.getTrytes(approve_hash["branchTransaction"])

            #今は代わりにハッシュが表示されるようにしてる
            #今はdepthをインクリしていっている
            #あと回数制限もうけて承認なしでも送れるようにしておく
            approve = False
            print(trunk_bundle)
            if not trunk_bundle in self.ignore_bundle:
                while approve != True:
                    approve = self.approve_tx(trunk_image)
                    if approve == False:
                        depth += 5
                        approve_hash = self.trunk_and_branch(depth)
                        print(approve_hash["trunkTransaction"])
                transaction.trunk_trasaction_hash = approve_hash["trunkTransaction"]

            approve = False
            if not branch_bundle in self.ignore_bundle:
                while approve != True:
                    approve = self.approve_tx(branch_image)
                    if approve == False:
                        depth += 5
                        approve_hash = self.trunk_and_branch(depth)
                        print(approve_hash["branchTransaction"])
                transaction.branch_trasaction_hash = approve_hash["branchTransaction"]

        bundle.finalize()
        self.bundle_tryte = bundle.as_tryte_strings()

    def approve_tx(self, image):
        img_msg = str(self.combine_tryte(image))
        if len(img_msg) % 2 == 1:
            img_msg = img_msg[:-1]
        from_tryte_to_picture(TryteString(img_msg))
        w = input("[y/n]")
        if w == "y":
            return True
        elif w == "n":
            return False

    def trunk_and_branch(self, depth):
        command = {
            "command" : "getTransactionsToApprove",
            "depth": depth,
        }
        stringified = json.dumps(command)

        headers = {
            "content-type" : "application/json",
            "X-IOTA-API-Version" : "1",
        }
        request = urllib.request.Request(url = self.args.host_ip, data = stringified.encode("utf-8"), headers = headers)
        returnData = urllib.request.urlopen(request).read()

        return json.loads(returnData)

    def attach(self):
        trunk_branch_hash = self.trunk_and_branch()
        self.api.attach_to_tangle(trunk_branch_hash["trunkTransaction"], trunk_branch_hash["branchTransaction"], self.bundle_tryte)

    def send_tx(self):
        depth = 5
        print(self.api.send_transfer(depth, self.tx))

    def send_tryte(self):
        depth = 5
        print(self.api.send_trytes(self.trytes["trytes"], depth))

    def new_address(self, index, count):
        return self.api.get_new_addresses(index, count)

    def combine_tryte(self, image):
        index = []
        trytes = [_ for _ in range(len(image))]
        tryte = TryteString.from_string("")
        for fragment in image:
            index = int(fragment.signature_message_fragment[0:8].as_string()[0:3])
            trytes[index] = fragment.signature_message_fragment[8:]
        else:
            for val in trytes:
                tryte += val
        return tryte
