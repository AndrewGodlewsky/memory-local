"""Run bundled OptMem using only the store beside this repository's tools."""

from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import os
from pathlib import Path
import sys


def main():
    here = Path(__file__).resolve().parent
    root = here.parent.parent
    memory = root / ".optmem"
    # Reject redirected stores, including a redirected record inside the tree.
    candidates = [memory]
    if memory.is_dir():
        candidates.extend(memory.rglob("*"))
    for path in candidates:
        if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
            sys.exit("Repository memory paths must not be symlinks or junctions: " + str(path))
        try:
            path.resolve().relative_to(root)
        except ValueError:
            sys.exit("Repository memory path escapes the repository: " + str(path))
    os.environ["MEMORY_DIR"] = str(memory)
    sys.dont_write_bytecode = True
    loader = SourceFileLoader("repo_memory_optmem", str(here / "vendor" / "memo"))
    spec = spec_from_loader(loader.name, loader)
    cli = module_from_spec(spec)
    loader.exec_module(cli)
    cli.ME = 'python "' + str(Path(__file__).resolve()) + '"'
    cli.main()


if __name__ == "__main__":
    main()
