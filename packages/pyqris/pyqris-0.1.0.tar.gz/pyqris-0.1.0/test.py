from pathlib import Path
import sys

sys.path.insert(0, (Path(__file__).parent / "target/debug").__str__())
import libpyqris  # type: ignore

r = libpyqris.QRIS("/home/krypton-byte/Downloads/test.jpeg")
d = r.to_dict()
ss = libpyqris.QRIS.from_dict(r.to_dict())
ss.save("anjay.png", 500)
print(ss.dumps())
