"""Integration checks for repo-memory setup and the real pinned OptMem CLI.

These checks establish storage behavior, not whether an agent selects or recalls
the right project knowledge. Fresh-context agent evaluation is a separate trial.
Run: python -m unittest discover -s tests -v
"""

import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import uuid


SOURCE_ROOT = Path(__file__).resolve().parents[1]
SETUP = SOURCE_ROOT / "skills" / "repo-memory" / "scripts" / "setup.py"
PINNED_COMMIT = "1fb164cf39028047781f72ac3bb1e5a691c1dcb0"


class RepoMemorySetupTests(unittest.TestCase):
    def setUp(self):
        # Python 3.13's mkdtemp mode 0700 creates an inaccessible directory under
        # the Windows restricted-token runner. Inherit the permitted temp ACL.
        self.root = Path(tempfile.gettempdir()) / ("repo memory tests " + uuid.uuid4().hex)
        self.root.mkdir()
        self.addCleanup(self.clean_sandbox)
        self.repo = self.new_repo("project with spaces")
        self.foreign = self.root / "foreign store"
        self.foreign.mkdir()
        (self.foreign / "sentinel.txt").write_text("untouched", encoding="utf-8")
        self.env = os.environ.copy()
        self.env["MEMORY_DIR"] = str(self.foreign)
        self.env["PYTHONIOENCODING"] = "utf-8"

    def clean_sandbox(self):
        target = self.root.resolve()
        self.assertEqual(target.parent, Path(tempfile.gettempdir()).resolve())
        self.assertTrue(target.name.startswith("repo memory tests "))

        def remove_readonly(function, path, exception):
            # Git objects are read-only on Windows. Clear that attribute only
            # inside this test's verified disposable root, then retry removal.
            self.assertTrue(Path(path).resolve().is_relative_to(target))
            if not isinstance(exception[1], PermissionError):
                raise exception[1]
            os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
            function(path)

        shutil.rmtree(target, onerror=remove_readonly)

    def command(self, argv, *, cwd=None, success=True, env=None):
        result = subprocess.run(
            [str(arg) for arg in argv], cwd=cwd or self.repo,
            env=env or self.env, capture_output=True, text=True,
            encoding="utf-8", timeout=30,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def new_repo(self, name):
        path = self.root / name
        path.mkdir()
        result = subprocess.run(
            ["git", "init", "--quiet", str(path)], capture_output=True,
            text=True, encoding="utf-8", timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return path

    def install(self, repo=None, *, success=True):
        return self.command([sys.executable, SETUP, "--repo", repo or self.repo], success=success)

    def memo(self, *args, repo=None, cwd=None, success=True):
        launcher = (repo or self.repo) / "tools" / "memory" / "memo.py"
        return self.command([sys.executable, launcher, *args], cwd=cwd, success=success)

    @staticmethod
    def snapshot(path):
        return {str(file.relative_to(path)): file.read_bytes()
                for file in path.rglob("*") if file.is_file()}

    def test_setup_creates_empty_ignored_store_and_trackable_launcher(self):
        self.install()
        self.assertEqual((self.repo / ".optmem" / "LOG.txt").read_bytes(), b"")
        self.assertTrue((self.repo / ".optmem" / "TREE").is_dir())
        self.assertTrue((self.repo / ".optmem" / "config").is_file())
        self.command(["git", "check-ignore", "--quiet", ".optmem/LOG.txt"])
        self.command(["git", "check-ignore", "--quiet", "tools/memory/memo.py"], success=False)
        instructions = (self.repo / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("tools/memory/", instructions)
        self.memo("wake")
        self.assertEqual(self.snapshot(self.foreign), {"sentinel.txt": b"untouched"})

    def test_upstream_pin_and_digest_describe_installed_bytes(self):
        self.install()
        vendor = self.repo / "tools" / "memory" / "vendor"
        metadata = json.loads((vendor / "source.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["commit"], PINNED_COMMIT)
        self.assertEqual(metadata["repository"].rstrip("/"), "https://github.com/VictorTaelin/OptMem")
        self.assertEqual(metadata["sha256"], hashlib.sha256((vendor / "memo").read_bytes()).hexdigest())

    def test_upstream_bytes_survive_git_round_trip_with_autocrlf(self):
        self.install()
        vendor_path = "tools/memory/vendor"
        original = (self.repo / vendor_path / "memo").read_bytes()
        metadata = json.loads((self.repo / vendor_path / "source.json").read_text(encoding="utf-8"))
        git = ["git", "-c", "core.autocrlf=true"]
        self.command([*git, "add", "--", vendor_path])
        # Read the actual staged blob as bytes; text subprocess decoding would
        # normalize CRLF and hide the very corruption this regression checks.
        staged = subprocess.run(
            [*git, "show", ":" + vendor_path + "/memo"], cwd=self.repo,
            env=self.env, capture_output=True, timeout=30,
        )
        self.assertEqual(staged.returncode, 0, staged.stderr)
        self.assertEqual(staged.stdout, original)
        self.assertEqual(hashlib.sha256(staged.stdout).hexdigest(), metadata["sha256"])
        checkout = self.root / "checkout with spaces"
        checkout.mkdir()
        self.command([*git, "checkout-index", "--all", "--prefix=" + checkout.as_posix() + "/"])
        checked_out = (checkout / vendor_path / "memo").read_bytes()
        self.assertEqual(checked_out, original)
        self.assertEqual(hashlib.sha256(checked_out).hexdigest(), metadata["sha256"])

    def test_notes_and_configuration_survive_exact_setup_rerun(self):
        agents = b"# Project rules\r\n\r\nAlways use the existing API.\r\n"
        ignores = b"# Existing exclusions\r\n/build/\r\n"
        (self.repo / "AGENTS.md").write_bytes(agents)
        (self.repo / ".gitignore").write_bytes(ignores)
        self.install()
        self.memo("note", "Decision: keep SQLite because the prototype needs no database service.")
        self.memo("config", "WAKE_LINES=3")
        before = self.snapshot(self.repo / ".optmem")
        agents_after = (self.repo / "AGENTS.md").read_bytes()
        ignores_after = (self.repo / ".gitignore").read_bytes()
        self.assertIn(agents, agents_after)
        self.assertIn(ignores, ignores_after)
        self.install()
        self.assertEqual(self.snapshot(self.repo / ".optmem"), before)
        self.assertEqual((self.repo / "AGENTS.md").read_bytes(), agents_after)
        self.assertEqual((self.repo / ".gitignore").read_bytes(), ignores_after)
        self.assertIn("no database service", self.memo("recall", "SQLite").stdout)

    def test_memory_stays_with_launcher_across_cwds_and_inherited_environment(self):
        self.install()
        other = self.new_repo("other project")
        self.install(other)
        nested = other / "src" / "nested folder"
        nested.mkdir(parents=True)
        self.memo("note", "Decision: project alpha uses SQLite for deployment simplicity.", cwd=nested)
        self.memo("note", "Decision: project beta uses Postgres for existing infrastructure.", repo=other)
        alpha = self.memo("recall", "SQLite|Postgres", cwd=nested).stdout
        beta = self.memo("recall", "SQLite|Postgres", repo=other).stdout
        self.assertIn("project alpha", alpha)
        self.assertNotIn("project beta", alpha)
        self.assertIn("project beta", beta)
        self.assertNotIn("project alpha", beta)
        self.assertEqual(self.snapshot(self.foreign), {"sentinel.txt": b"untouched"})

    def test_missing_store_fails_without_creating_or_redirecting_memory(self):
        self.install()
        store = self.repo / ".optmem"
        store.rename(self.repo / "saved memory")
        self.memo("wake", success=False)
        self.memo("note", "This must not silently create a replacement store.", success=False)
        self.assertFalse(store.exists())
        self.assertEqual(self.snapshot(self.foreign), {"sentinel.txt": b"untouched"})

    def test_real_summary_cycle_preserves_original_evidence(self):
        self.install()
        self.memo("config", "WAKE_LINES=1")
        first = "Decision: use SQLite because deployment must need no database service."
        second = "Constraint: this database choice is scoped to the prototype, not production."
        summary = "Prototype storage uses SQLite to avoid running a database service; production remains undecided."
        self.memo("note", first)
        request = self.memo("note", second).stdout
        self.assertIn(first, request)
        self.assertIn(second, request)
        self.assertIn("nap 0-1", request)
        before = (self.repo / ".optmem" / "LOG.txt").read_bytes()
        self.memo("wake", success=False)
        self.memo("nap", "0-1", summary)
        wake = self.memo("wake").stdout
        self.assertIn(summary, wake)
        self.assertNotIn(first, wake)
        expanded = self.memo("zoom", "0-1").stdout
        self.assertIn(first, expanded)
        self.assertIn(second, expanded)
        recalled = self.memo("recall", "SQLite|production").stdout
        self.assertIn(first, recalled)
        self.assertIn(second, recalled)
        self.assertEqual((self.repo / ".optmem" / "LOG.txt").read_bytes(), before)

    def test_invalid_note_does_not_mutate_log(self):
        self.install()
        self.memo("note", "Accepted decision with a durable reason.")
        before = (self.repo / ".optmem" / "LOG.txt").read_bytes()
        self.memo("note", "a" * 281, success=False)
        self.memo("note", "line one\nline two", success=False)
        self.assertEqual((self.repo / ".optmem" / "LOG.txt").read_bytes(), before)

    def test_setup_requires_git_root_and_does_not_touch_nested_folder(self):
        ordinary = self.root / "not a repository"
        ordinary.mkdir()
        self.install(ordinary, success=False)
        self.assertEqual(list(ordinary.iterdir()), [])
        nested = self.repo / "src"
        nested.mkdir()
        self.install(nested, success=False)
        self.assertEqual(list(nested.iterdir()), [])
        self.assertFalse((self.repo / ".optmem").exists())

    def test_differing_existing_launcher_is_preserved(self):
        target = self.repo / "tools" / "memory" / "memo.py"
        target.parent.mkdir(parents=True)
        existing = b"# Existing user-owned launcher\n"
        target.write_bytes(existing)
        self.install(success=False)
        self.assertEqual(target.read_bytes(), existing)
        self.assertFalse((self.repo / ".optmem").exists())


if __name__ == "__main__":
    unittest.main()
