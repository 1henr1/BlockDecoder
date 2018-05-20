# encoding: UTF-8

import binascii


def print_function_name(func):
    """简单装饰器用于输出函数名"""
    def wrapper(*args, **kw):
        print(str(func.__name__))
        return func(*args, **kw)
    return wrapper


def print_dict(obj):
    sample = dict()
    for (k, v) in obj.items():
        if type(v) == type(sample):
            print('(', k, ':')
            print_dict(v)
            print(')')
        else:
            print('(', k, ':', v, ')')


class CBlockHeader(object):
    """ bitcoin header definition """

    def __init__(self):
        pass


class BlockDecoder(object):
    """ bitcoin block decoder """
    BITCOIN_HEADER_SIZE = 80

    def __init__(self):
        self.header = {}
        self.body = {}

        pass

    def clear(self):
        pass

    def decode_block(self, stream):
        self.decode_header(stream)
        print_dict(self.header)
        self.decode_body(stream)
        print_dict(self.body)

    def decode_header(self, stream):
        self.header["nVersion"] = int.from_bytes(stream.read(4), byteorder='little')
        self.header["hashPrevBlock"] = self.decode_hash(stream.read(32))
        self.header["hashMerkleRoot"] = self.decode_hash(stream.read(32))
        self.header["nTime"] = int.from_bytes(stream.read(4), byteorder='little')
        self.header["nBits"] = int.from_bytes(stream.read(4), byteorder='little')
        self.header["nNonce"] = int.from_bytes(stream.read(4), byteorder='little')

    def decode_body(self, stream):
        txn_count = self.decode_compact_size(stream)
        self.body["txn_count"] = txn_count
        self.body["tx"] = list()
        for i in range(txn_count):
            self.body["tx"].append(self.decode_transaction(stream))
        return

    def decode_transaction(self, stream):
        ret = dict()
        ret["version"] = int.from_bytes(stream.read(4), byteorder='little')
        ret["tx_in_count"] = self.decode_compact_size(stream)
        ret["tx_in"] = list()
        for i in range(ret["tx_in_count"]):
            ret["tx_in"].append(self.decode_tx_in(stream))
        ret["tx_out_count"] = self.decode_compact_size(stream)
        ret["tx_out"] = list()
        for i in range(ret["tx_out_count"]):
            ret["tx_out"].append(self.decode_tx_out(stream))
        ret["lock_time"] = int.from_bytes(stream.read(4), byteorder='little')
        return ret

    def decode_tx_in(self, stream):
        ret = dict()
        ret["previous_output"] = self.decode_outpoint(stream)
        ret["script_size"] = self.decode_compact_size(stream)
        ret["script"] = binascii.b2a_hex(stream.read(ret["script_size"])).decode('ascii')
        ret["sequence"] = int.from_bytes(stream.read(4), byteorder='little')
        return ret

    def decode_outpoint(self, stream):
        ret = dict()
        ret["hash"] = self.decode_hash(stream.read(32))
        ret["index"] = int.from_bytes(stream.read(4), byteorder='little')
        return ret

    def decode_tx_out(self, stream):
        ret = dict()
        ret["value"] = int.from_bytes(stream.read(8), byteorder='little') / 100000000.0
        ret["script_size"] = self.decode_compact_size(stream)
        ret["pk_script"] = binascii.b2a_hex(stream.read(ret["script_size"])).decode('ascii')
        return ret

    def decode_hash(self, byte_array):
        hex_array = [hex(byte)[2:] for byte in byte_array]
        hex_array.reverse()
        return ''.join(hex_array)

    def decode_compact_size(self, stream):
        first_byte = int.from_bytes(stream.read(1), byteorder='little')
        if first_byte < 253:
            ret = first_byte
        elif first_byte == 253:
            ret = int.from_bytes(stream.read(2), byteorder='little')
        elif first_byte == 254:
            ret = int.from_bytes(stream.read(4), byteorder='little')
        elif first_byte == 255:
            ret = int.from_bytes(stream.read(8), byteorder='little')
        return ret

    def output(self):
        ret = dict()
        ret["header"] = self.header
        ret["body"] = self.body
        return ret
