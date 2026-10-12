"""Run the pinned OptMem CLI against this demo's store, from any directory."""
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    os.environ["MEMORY_DIR"] = str(ROOT / ".optmem")
    loader = SourceFileLoader("optmem_demo_cli", str(ROOT / "tools" / "memo"))
    spec = spec_from_loader(loader.name, loader)
    cli = module_from_spec(spec)
    loader.exec_module(cli)
    # Make the tool's suggested follow-up commands usable in PowerShell.
    cli.ME = 'python "' + str(Path(__file__).resolve()) + '"'
    cli.main()


if __name__ == "__main__":
    main()
