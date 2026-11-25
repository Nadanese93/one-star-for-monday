"""Write the One Star for Monday entry to /output/entry.txt."""

import os
import tempfile

ENTRY = "One star. Ordered the Monday special \u2014 a cold inbox, a warm laptop, and a waiter who kept refilling my deadlines."


def main() -> None:
    if not ENTRY or not ENTRY.strip() or not 1 <= len(ENTRY) <= 180:
        raise ValueError("entry must be 1-180 characters and not whitespace-only")
    if len(ENTRY.split()) > 25:
        raise ValueError("entry must be at most 25 words")
    if "\n" in ENTRY or "\r" in ENTRY:
        raise ValueError("entry must be a single line")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(ENTRY)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
