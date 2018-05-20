# encoding UTF-8

import sys
import os
import json
from Block_Decoder import BlockDecoder

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./Block_Decoder.py  block_path")
        exit(0)

    block_path = sys.argv[1]
    if not os.path.exists(block_path):
        print("block is not existed")
        exit(0)

    with open(block_path, 'rb') as block:
        decoder = BlockDecoder()
        decoder.decode_block(block)
        res = decoder.output()
        with open("decode.json", "w") as f:
            json.dump(res, f, indent=2)


