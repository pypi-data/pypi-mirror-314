import base64 as b64
import marshal as ms
import zlib as zb
import gzip as gz
import codecs as cd
import time as tm
def b6(code):
    encoded = b64.b64encode(code.encode()).decode()
    return "import base64;exec(base64.b64decode('" + encoded + "'))"
def b3(code):
    encoded = b64.b32encode(code.encode()).decode()
    return "import base64;exec(base64.b32decode('" + encoded + "'))"
def lb(code):
    compressed = zb.compress(code.encode('utf-8'))
    return "import zlib;exec(zlib.decompress(" + repr(compressed) + ").decode())"
def zb_enc(code):
    compressed = zb.compress(code.encode('utf-8'))
    encoded = b64.b64encode(compressed).decode()
    return "import zlib\nimport base64\nexec(zlib.decompress(base64.b64decode('" + encoded + "')).decode())"
def gz_enc(code):
    compressed = gz.compress(code.encode())
    encoded = b64.b64encode(compressed).decode()
    return "import gzip\nimport base64\nexec(gzip.decompress(base64.b64decode('" + encoded + "')).decode())"
def ms_enc(code):
    compiled = compile(code, '<string>', 'exec')
    encrypted = b64.b64encode(ms.dumps(compiled))
    return "import marshal\nimport base64\nexec(marshal.loads(base64.b64decode('" + encrypted.decode() + "')))"
def hx(code):
    encoded = code.encode().hex()
    return "exec(bytes.fromhex('" + encoded + "'))"
def mz_enc(code):
    compiled = compile(code, "<string>", 'exec')
    marshaled = ms.dumps(compiled)
    compressed = zb.compress(marshaled)
    return "import zlib;import marshal;exec(marshal.loads(zlib.decompress(" + repr(compressed) + ")))"
def r13(code):
    encoded = cd.encode(code, 'rot_13')
    return """import codecs;exec(codecs.decode({}, 'rot_13'))""".format(repr(encoded))
def ef(fn, efns):
    with open(fn, "r", encoding="utf-8") as f:
        code = f.read()
    for fnc in efns:
        code = fnc(code)
        tm.sleep(2)
    out = "enc-" + fn.split('.')[0] + ".py"
    with open(out, "w", encoding="utf-8") as enc_file:
        enc_file.write("# -*- coding: utf-8 -*-\n")
        enc_file.write(code)
    return out