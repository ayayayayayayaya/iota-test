#/usr/bin/env python
# -*- coding: utf-8 -*-

from iota import *
from getTransaction import getTransaction
import json
import urllib

class IOTA:
    def __init__(self, args):
        self.api = Iota(args.host_ip, args.seed)
        self.tx = []
        self.args = args
        self.getTransaction = getTransaction(args)
        self.done_approvee_bundle = []

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

    def prepare_trytes(self):
        for i in range(len(self.tx)):
            prev_tx = None
            trunk_branch_hash = self.trunk_and_branch()
            #self.attach(trunk_branch_hash)
            trunk_txn, trunk_bundle = self.getTransaction.getTrytes(trunk_branch_hash["trunkTransaction"])
            branch_txn, branch_bundle = self.getTransaction.getTrytes(trunk_branch_hash["branchTransaction"])

            for trunk_tx in trunk_txn:
                if trunk_tx.bundle_hash not in self.done_approvee_bundle:
                    #確認するトランザクションリストに追加
                    self.done_approvee_bundle.append(trunk_tx.bundle_hash)

            for trunk_tx_bundle in trunk_bundle:
                if trunk_tx_bundle.bundle_hash not in self.done_approvee_bundle:
                    #確認するトランザクションリストに追加
                    self.done_approvee_bundle.append(trunk_tx_bundle.bundle_hash)

            for branch_tx in branch_txn:
                if branch_tx.bundle_hash not in self.done_approvee_bundle:
                    #確認するトランザクションリストに追加
                    self.done_approvee_bundle.append(branch_tx.bundle_hash)

            for branch_tx_bundle in branch_bundle:
                if branch_tx_bundle.bundle_hash not in self.done_approvee_bundle:
                    #確認するトランザクションリストに追加
                    self.done_approvee_bundle.append(branch_tx_bundle.bundle_hash)

            self.tx[i].trunk_transaction_hash = trunk_branch_hash["trunkTransaction"] if prev_tx is None else prev_tx.hash
            self.tx[i].branch_transaction_hash = trunk_branch_hash["branchTransaction"] if prev_tx is None else trunk_hash

        if self.tx[0].trunk_transaction_hash not in self.done_approvee_bundle:
            #画像確認
            print(self.tx[0].trunk_transaction_hash)
        if self.tx[0].branch_transaction_hash not in self.done_approvee_bundle:
            #画像確認
            print(self.tx[0].branch_transaction_hash)

        self.trytes = self.api.prepare_transfer(self.tx)

    def set_bundle(self):
        bundle = ProposedBundle()
        for transaction in self.tx:
            bundle.add_transaction(transaction)

        bundle.finalize()
        self.bundle_tryte = bundle.as_tryte_strings()

    def trunk_and_branch(self):
        command = {
            "command" : "getTransactionsToApprove",
            "depth": 5,
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

    def combine_tryte(self, trytes_list):
        combined_trytes = TryteString("")
        for i in trytes_list:
            combined_trytes += i
        return combined_trytes
