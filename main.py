"""news-image-20261122 entrypoint.

Copies the entry image (entry.png, stored next to this file) to the
output directory the grader expects: /output, or $MAKEFUN_OUTPUT_DIR
for local runs. After copying, it checks the copy byte-for-byte
against the source with SHA-256 so a truncated write is caught.

Stdlib only, no network access.
"""

import hashlib
import os
import shutil
import sys

CHUNK = 1 << 20


def digest(path):
    """SHA-256 hex digest of a file, streamed in 1 MiB chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(CHUNK)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(base, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(source):
        print(f"error: entry image not found: {source}", file=sys.stderr)
        return 1

    shutil.copyfile(source, target)

    source_digest = digest(source)
    target_digest = digest(target)
    if source_digest != target_digest:
        print("self-check FAILED: copy differs from source", file=sys.stderr)
        return 1
    if os.path.getsize(source) != os.path.getsize(target):
        print("self-check FAILED: size mismatch after copy", file=sys.stderr)
        return 1
    print(f"entry.png written to {target} (sha256 {target_digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
