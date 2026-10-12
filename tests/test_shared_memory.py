"""Exercise shared knowledge with independent local Git clones."""

import json
import sys
import unittest

import test_repo_memory_setup as base


class SharedMemoryTests(unittest.TestCase):
    setUp = base.RepoMemorySetupTests.setUp
    clean_sandbox = base.RepoMemorySetupTests.clean_sandbox
    command = base.RepoMemorySetupTests.command
    new_repo = base.RepoMemorySetupTests.new_repo
    memo = base.RepoMemorySetupTests.memo

    def install(self, *args, repo=None, success=True):
        return self.command([sys.executable, base.SETUP, "--repo", repo or self.repo, *args], success=success)

    def commit(self, repo, message):
        self.command(["git", "add", "--all"], cwd=repo)
        self.command(["git", "-c", "user.name=Memory Test", "-c", "user.email=memory@example.invalid",
                      "commit", "--quiet", "-m", message], cwd=repo)

    def test_existing_authority_is_preserved_and_selected_on_rerun(self):
        source = self.repo / "decisions" / "intent.md"
        source.parent.mkdir()
        content = b"# Existing decisions\r\n\r\nPrototype: CSV only; PDF deferred.\r\n"
        source.write_bytes(content)
        self.install("--shared-memory", "decisions/intent.md")
        self.assertFalse((self.repo / "docs/project-memory.md").exists())
        self.assertEqual(source.read_bytes(), content)
        self.memo("note", "History: export decision lives in decisions/intent.md")
        log = (self.repo / ".optmem/LOG.txt").read_bytes()
        self.install()
        self.assertEqual(source.read_bytes(), content)
        self.assertEqual((self.repo / ".optmem/LOG.txt").read_bytes(), log)
        config = json.loads((self.repo / "tools/memory/config.json").read_text())
        self.assertEqual(config["shared_memory"], "decisions/intent.md")
        self.assertIn("decisions/intent.md", (self.repo / "AGENTS.md").read_text())
        self.install("--shared-memory", "other.md", success=False)
        self.assertFalse((self.repo / "other.md").exists())

    def test_independent_clones_share_committed_authority_without_local_history(self):
        self.install()
        authority = self.repo / "docs/project-memory.md"
        authority.write_text("# Shared project knowledge\n", encoding="utf-8")
        self.commit(self.repo, "Install shared memory integration")
        clones = []
        for name in ("contributor A", "contributor B"):
            target = self.root / name
            self.command(["git", "clone", "--local", "--quiet", self.repo.as_posix(), target.as_posix()])
            clones.append(target)
        first, second = clones
        self.assertFalse((first / ".optmem").exists())
        self.assertFalse((second / ".optmem").exists())
        self.memo("init", repo=first)
        self.memo("note", "Private observation: local experiment costs 37 seconds.", repo=first)
        decision = "Export decision: prototype uses CSV only because the importer accepts CSV; production is undecided.\n"
        (first / "docs/project-memory.md").write_text("# Shared project knowledge\n\n" + decision, encoding="utf-8")
        self.assertNotIn(decision.strip(), (second / "docs/project-memory.md").read_text())
        self.commit(first, "Record scoped export decision")
        # B receives A's committed branch through a normal pull; no filesystem
        # copying of the ignored store or original conversation occurs.
        self.command(["git", "pull", "--quiet", "--ff-only", first.as_posix(), "HEAD"], cwd=second)
        self.assertIn(decision.strip(), (second / "docs/project-memory.md").read_text())
        self.assertFalse((second / ".optmem").exists())
        self.memo("init", repo=second)
        self.assertEqual((second / ".optmem/LOG.txt").read_bytes(), b"")
        recalled = self.memo("recall", "Private observation", repo=second)
        self.assertNotIn("37 seconds", recalled.stdout)
        self.assertIn("37 seconds", self.memo("recall", "Private observation", repo=first).stdout)
        self.command(["git", "check-ignore", "--quiet", ".optmem/LOG.txt"], cwd=second)
        tracked = self.command(["git", "ls-files"], cwd=second).stdout
        self.assertNotIn(".optmem/", tracked)
        for relative in ("AGENTS.md", "docs/project-memory.md", "tools/memory/config.json"):
            content = (second / relative).read_text(encoding="utf-8")
            self.assertNotIn(str(first), content)
            self.assertNotIn("37 seconds", content)
        # Working-tree-only knowledge is not present in B even after a pull.
        with (first / "docs/project-memory.md").open("a", encoding="utf-8") as file:
            file.write("Uncommitted observation: desktop export remains slow.\n")
        self.command(["git", "pull", "--quiet", "--ff-only", first.as_posix(), "HEAD"], cwd=second)
        self.assertNotIn("desktop export remains slow", (second / "docs/project-memory.md").read_text())

    def test_unsafe_or_private_shared_paths_are_rejected_before_install(self):
        for path in ("../outside.md", str(self.root / "outside.md"), ".optmem/notes.md", "AGENTS.md", "tools", "."):
            with self.subTest(path=path):
                self.install("--shared-memory", path, success=False)
                self.assertFalse((self.repo / "tools/memory").exists())
        (self.repo / ".gitignore").write_text("private/\n")
        self.install("--shared-memory", "private/decisions.md", success=False)
        self.assertFalse((self.repo / "tools/memory").exists())


if __name__ == "__main__":
    unittest.main()
