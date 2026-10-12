"""Small, isolated CLI demonstration; no API calls or installed integration."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
store = Path(tempfile.mkdtemp(prefix="store-", dir=ROOT))
env = dict(os.environ, MEMORY_DIR=str(store))
steps = []


def run(*args, expected=0):
    result = subprocess.run(
        [sys.executable, str(ROOT / "memo"), *args], env=env,
        capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    steps.append(dict(args=args, code=result.returncode,
                      stdout=result.stdout, stderr=result.stderr))
    assert result.returncode == expected, steps[-1]
    return result.stdout


run("init")
run("config", "WAKE_LINES=2")
run("note", "DEMO decision: use SQLite for the prototype; no database server needed.")
run("note", "DEMO failed approach: JSON writes lost updates under concurrent workers.")
run("note", "DEMO correction: use PostgreSQL for production; SQLite remains prototype-only.")
assert "Cannot wake" in run("wake", expected=1)
run("nap", "0-1", "DEMO: SQLite selected for prototype simplicity; JSON writes lost updates under concurrent workers.")
assert "PostgreSQL" in run("wake")
assert "JSON writes lost updates" in run("recall", "JSON")
assert "database server" in run("zoom", "0-1")
before = (store / "LOG.txt").read_bytes()
run("forget", "0-1")
assert before == (store / "LOG.txt").read_bytes()
assert "Cannot wake" in run("wake", expected=1)
run("nap", "0-1", "DEMO: Prototype uses SQLite to avoid a DB server. Concurrent JSON writes lost updates.")
run("wake")
run("note", "x" * 281, expected=1)
assert before == (store / "LOG.txt").read_bytes()
report = dict(
    scope="Mechanics only, synthetic notes and explicitly supplied summaries; not a memory-quality benchmark",
    python=sys.version, store=str(store), passed=True, steps=steps,
)
(ROOT / "smoke-results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({"passed": True, "commands": len(steps), "store": str(store)}))
