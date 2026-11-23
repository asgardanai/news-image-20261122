"""Copy entry.png next to this script into the output folder.

The output folder comes from MAKEFUN_OUTPUT_DIR, falling back to
/output when that variable is not set. The copy is verified
byte-for-byte by comparing SHA-256 digests of source and target.
"""

import hashlib
import os
import shutil
import sys


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")

    if not os.path.isfile(source):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)

    target = os.path.join(output_dir, "entry.png")
    shutil.copyfile(source, target)

    if os.path.getsize(source) != os.path.getsize(target):
        print("error: copied file size does not match entry.png", file=sys.stderr)
        return 1

    if sha256_of(source) != sha256_of(target):
        print("error: copied file does not match entry.png", file=sys.stderr)
        return 1

    print(f"copied entry.png to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
