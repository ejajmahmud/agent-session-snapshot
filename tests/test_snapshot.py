"""Tests for agent-session-snapshot."""
import unittest
from agent_session_snapshot.snapshot import SessionSnapshot


class TestSessionSnapshot(unittest.TestCase):
    def setUp(self):
        self.snap = SessionSnapshot()

    def test_capture_and_restore(self):
        original = {"step": 42, "variables": {"user": "bob", "auth": True}}
        chk_id, h = self.snap.capture_snapshot("sess_1", original)
        restored = self.snap.restore_snapshot(chk_id)
        self.assertEqual(restored, original)

    def test_base64_portability(self):
        original = {"task": "deploy"}
        chk_id, _ = self.snap.capture_snapshot("sess_2", original)
        b64_str = self.snap.export_snapshot_base64(chk_id)
        self.snap.import_snapshot_base64("sess_2_imported", b64_str)
        self.assertEqual(self.snap.restore_snapshot("sess_2_imported"), original)


if __name__ == "__main__":
    unittest.main()
