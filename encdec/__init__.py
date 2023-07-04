#!/usr/bin/env python3

def _main():
    # $0 [infile] -o <outfile>
    # if infile is not specified, read from stdin
    # if outfile is not specified, write to stdout
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Encode or decode a file.')
    parser.add_argument('input', nargs='?', type=argparse.FileType('rb'), default=sys.stdin.buffer)
    parser.add_argument('-o', '--output', type=argparse.FileType('wb'), default=sys.stdout.buffer)
    args = parser.parse_args()
    return (args.input, args.output)

def encode(encdec_class):
    i, o = _main()
    encdec_class().encode(i, o)

def decode(encdec_class):
    i, o = _main()
    encdec_class().decode(i, o)


# a decoding and encoding function
class EncDec:
    def encode(self, i, o):
        raise NotImplementedError
    def decode(self, i, o):
        raise NotImplementedError

class StreamEncDec(EncDec):
    def __init__(self, enc_func, dec_func):
        self.enc_func = enc_func
        self.dec_func = dec_func
    
    def encode(self, i, o):
        o.write(self.enc_func(i.read()))

    def decode(self, i, o):
        o.write(self.dec_func(i.read()))

class ByteStreamEncDec(EncDec):
    def __init__(self, enc_func, dec_func):
        # takes a byte, returns a byte
        self.enc_func = enc_func
        self.dec_func = dec_func

    def encode(self, i, o):
        while (b := i.read(1)):
            o.write(self.enc_func(b))

    def decode(self, i, o):
        while (b := i.read(1)):
            o.write(self.dec_func(b))

class HexEncDec(ByteStreamEncDec):
    def __init__(self, **args):
        super().__init__(lambda x: bytes([*x]).hex().encode(), lambda x: bytes.fromhex(x.decode(errors='ignore')))

    def decode(self, i, o):
        while (b := i.read(2)):
            o.write(self.dec_func(b))


import urllib.parse
class UrlEncDec(ByteStreamEncDec):
    def __init__(self, **args):
        # use bytes (e.g. unquote_to_bytes) instead of str (e.g. unquote)
        super().__init__(lambda x: urllib.parse.quote(x).encode(), urllib.parse.unquote_to_bytes)

    decode = StreamEncDec.decode

import base64
class Base64EncDec(StreamEncDec):
    def __init__(self, **args):
        super().__init__(base64.b64encode, base64.b64decode)

