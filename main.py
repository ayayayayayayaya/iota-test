#/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import sys
import inspect
from c_iota import IOTA
from op_image import *
import random

def parse_argument():
    p = ArgumentParser()
    p.add_argument("host_ip", type = str)
    p.add_argument("seed", type = str)
    p.add_argument("--file", type = str)
    args = p.parse_args()
    try:
        if type(args.host_ip) is not str: raise ValueError("host_ip is must be string.")
        if type(args.seed) is not str: raise ValueError("seed is must be string.")
        if type(args.file) is not str: raise ValueError("filename is must be string.")
    except Exception as ex:
        print(ex, file = sys.stderr)
        sys.exit()
    return args

def main():
    args = parse_argument()
    tryte = to_tryte_from_picture(args)
    trytes = []
    print(type(tryte))
    for i in range(math.ceil(len(tryte) / 2187)):
        trytes.append(TryteString.from_string("{0:03d}_".format(i)) + tryte[0 + i * 2179 : 2179 + i * 2179])

    iota = IOTA(args)
    #iota.get_bundle()
    print("need tx num: " + str(len(trytes)))
    print(iota.node_info())
    address = iota.new_address(random.randint(0, 100),len(trytes))

    """
    #2187しか入らないからtryteを全部くっつけて画像に逆変換するための関数
    #from_tryte_to_picture(tryte)
    tryte = iota.combine_tryte(trytes)
    print(len(tryte))
    print(address)
    """
    if(iota.check_index()):
        iota.set_transaction(address["addresses"], trytes, ["TESTPIC" for _ in range(len(trytes))], [0 for _ in range(len(trytes))])
        #iota.prepare_trytes()
        #iota.send_tryte()

        iota.set_bundle()
        iota.attach()
        iota.send_tx()

    else:raise ValueError("LSMとKMがおかしい。しばらく待ってから再度施行")

if __name__ == "__main__":
    main()
