import base64
import marshal
import zlib
import gzip
import time
import codecs
import os
import sys
import time
import random
F = '\033[2;32m' #اخضر
B = '\x1b[38;5;208m' #برتقالي
S = '\033[1;33m'

def encode_file(file_name, encoding_functions):
    with open(file_name, "r", encoding="utf-8") as file:
        code = file.read()

    for encode_function in encoding_functions:
        code = encode_function(code)
        time.sleep(2) 

    with open("enc-" + file_name.split('.')[0] + ".py", "w", encoding="utf-8") as enc_file:
        enc_file.write("#https://t.me/ASH_TEAM\n# -*- coding: utf-8 -*-\n")
        enc_file.write(code)

def base64_encode(code):
    encoded_base64 = base64.b64encode(code.encode()).decode()
    return "import base64 as weashweashweashweashweash;exec(weashweashweashweashweash.b64decode('" + encoded_base64 + "'))"
def base32_encode(code):
    encoded_32 = base64.b32encode(code.encode()).decode()
    return "import base64 as wpebeoejebebejdirjnekdkdknebejfodoiebebskeoj288sjksbskeobejj;exec(wpebeoejebebejdirjnekdkdknebejfodoiebebskeoj288sjksbskeobejj.b32decode('" + encoded_32 + "'))"
def lambda_encode(code):
    compressed_data = zlib.compress(code.encode('utf-8'))
    return "import zlib as donotdecititiseasyashteam;exec(donotdecititiseasyashteam.decompress(" + repr(compressed_data) + ").decode())"
def zlib_encode(code):
    compressed_zlib = zlib.compress(code.encode('utf-8'))
    encoded_zlib = base64.b64encode(compressed_zlib).decode()
    return "import zlib\nimport base64\nexec(zlib.decompress(base64.b64decode('" + encoded_zlib + "')).decode())"
def gzip_encode(code):
    compressed_gzip = gzip.compress(code.encode())
    encoded_gzip = base64.b64encode(compressed_gzip).decode()
    return "import gzip\nimport base64\nexec(gzip.decompress(base64.b64decode('" + encoded_gzip + "')).decode())"
def marshal_encode(code):
    compiled_code = compile(code, '<string>', 'exec')
    encrypted_code = base64.b64encode(marshal.dumps(compiled_code, 10))
    return "import marshal\nimport base64\nexec(marshal.loads(base64.b64decode('" + encrypted_code.decode() + "')))"
def hex_encode(code):
    encoded_hex = code.encode().hex()
    return "exec(bytes.fromhex('" + encoded_hex + "'))"
def marshal_zlib_encode(code):
    compiled_code = compile(code, "<string>", 'exec')
    marshaled_code = marshal.dumps(compiled_code)
    compressed_code = zlib.compress(marshaled_code)
    encoded_code = "import zlib as AJQbsiEwViaOMwa==;import base64 as AJQbsiEwViaOWma==;import marshal as AJQbsiEwVia0Mwa==;exec(AJQbsiEwVia0Mwa==.loads(AJQbsiEwViaOMwa==.decompress(" + repr(compressed_code) + ")))"
    return encoded_code
def encoded_rot13(code):
    encoded_rot13 = codecs.encode(code, 'rot_13')
    return """import codecs;A= codecs.decode({0}, 'rot_13');exec(compile(A, filename="<ASH>", mode="exec"))""".format(repr(encoded_rot13))
file_name = input(f'{B} Enter Your File Name: {S} ')
encode_file(file_name, [base64_encode, base32_encode, lambda_encode, zlib_encode, gzip_encode, marshal_encode, marshal_zlib_encode, hex_encode ,encoded_rot13])
print(f'{F}Successfully encrypted file named enc-{file_name}!')