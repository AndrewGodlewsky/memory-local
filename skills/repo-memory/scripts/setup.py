"""Install the repo-memory evaluation in an explicitly selected Git root."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ASSETS = Path(__file__).resolve().parent.parent / "assets"
START = b"<!-- repo-memory:start -->"
END = b"<!-- repo-memory:end -->"
IGNORE_START = b"# repo-memory:start"
IGNORE_END = b"# repo-memory:end"


def guarded(root, path):
    """Validate every traversed path before creating or updating files."""
    current = root
    for part in path.relative_to(root).parts:
        current = current / part
        if current.is_symlink() or (hasattr(current, "is_junction") and current.is_junction()):
            raise ValueError("Refusing symlink or junction: " + str(current))
        if not current.resolve().is_relative_to(root):
            raise ValueError("Path escapes repository: " + str(current))
    return path


def merged_block(old, body, start, end):
    """Preserve all bytes outside the single managed block."""
    if old.count(start) != old.count(end) or old.count(start) > 1:
        raise ValueError("Malformed or duplicate repo-memory block; repair it before setup")
    newline = b"\r\n" if b"\r\n" in old else b"\n"
    body = body.replace(b"\r\n", b"\n").replace(b"\n", newline).rstrip(b"\r\n")
    if start in old:
        first, last = old.index(start), old.index(end)
        if last < first:
            raise ValueError("Reversed repo-memory block markers")
        return old[:first] + body + old[last + len(end):]
    separator = b"" if not old else (newline if old.endswith(b"\n") else newline * 2)
    return old + separator + body + newline


def install(repo):
    root = repo.expanduser().resolve(strict=True)
    git = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True,
    )
    if Path(git.stdout.strip()).resolve() != root:
        raise ValueError("--repo must name the Git root, not a subdirectory")

    source = json.loads((ASSETS / "vendor" / "source.json").read_text(encoding="utf-8"))
    vendor = (ASSETS / "vendor" / "memo").read_bytes()
    if hashlib.sha256(vendor).hexdigest() != source["sha256"]:
        raise ValueError("Bundled OptMem source does not match its recorded hash")

    files = {
        "tools/memory/memo.py": (ASSETS / "memo.py").read_bytes(),
        "tools/memory/vendor/memo": vendor,
        "tools/memory/vendor/source.json": (ASSETS / "vendor" / "source.json").read_bytes(),
        "tools/memory/vendor/.gitattributes": (ASSETS / "vendor" / ".gitattributes").read_bytes(),
    }
    writes = {}
    for relative, content in files.items():
        path = guarded(root, root / relative)
        if path.exists() and (not path.is_file() or path.read_bytes() != content):
            raise ValueError("Existing tool file differs; inspect it before replacing: " + str(path))
        if not path.exists():
            writes[path] = content
    for name, body, start, end in (
        ("AGENTS.md", (ASSETS / "instructions.md").read_bytes(), START, END),
        (".gitignore", b"# repo-memory:start\n/.optmem/\n# repo-memory:end\n", IGNORE_START, IGNORE_END),
    ):
        path = guarded(root, root / name)
        old = path.read_bytes() if path.exists() else b""
        replacement = merged_block(old, body, start, end)
        if replacement != old:
            writes[path] = replacement

    # Check all existing store paths before installing anything. Existing store
    # files, including customized config and summaries, are never rewritten.
    memory = guarded(root, root / ".optmem")
    if memory.exists() and not memory.is_dir():
        raise ValueError("Memory store is not a directory: " + str(memory))
    if memory.exists():
        for path in memory.rglob("*"):
            guarded(root, path)
    for name in ("LOG.txt", "config"):
        path = guarded(root, memory / name)
        if path.exists() and not path.is_file():
            raise ValueError("Expected memory file: " + str(path))
    tree = guarded(root, memory / "TREE")
    if tree.exists() and not tree.is_dir():
        raise ValueError("Expected summary directory: " + str(tree))

    for path, content in writes.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    # Upstream init only creates missing store files. Its global-identity setup
    # template is intentionally not installed; AGENTS.md uses repo-local scope.
    initialized = subprocess.run(
        [sys.executable, str(root / "tools/memory/memo.py"), "init"],
        capture_output=True, text=True, encoding="utf-8",
    )
    if initialized.returncode:
        raise ValueError("Installed files; memory initialization failed: " + initialized.stderr.strip())
    print("Repository memory ready: " + str(root))
    print("Local store: " + str(memory))
    print('Read memory: python "' + str(root / "tools/memory/memo.py") + '" wake')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path, help="Existing Git repository root")
    args = parser.parse_args()
    try:
        install(args.repo)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, "repo-memory setup: " + str(error) + "\n")


if __name__ == "__main__":
    main()
