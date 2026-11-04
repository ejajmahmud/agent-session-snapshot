"""State checkpoint and restoration engine for long-running agents."""
import json
import gzip
import base64
import hashlib
from typing import Dict, Any, Tuple


class SessionSnapshot:
    def __init__(self):
        self._checkpoints: Dict[str, bytes] = {}

    def capture_snapshot(self, session_id: str, state_data: Dict[str, Any]) -> Tuple[str, str]:
        """Serializes and compresses state. Returns (checkpoint_id, sha256_hash)."""
        raw_bytes = json.dumps(state_data, sort_keys=True).encode("utf-8")
        h = hashlib.sha256(raw_bytes).hexdigest()
        compressed = gzip.compress(raw_bytes)
        chk_id = f"{session_id}_{len(self._checkpoints) + 1}"
        self._checkpoints[chk_id] = compressed
        return chk_id, h

    def restore_snapshot(self, checkpoint_id: str) -> Dict[str, Any]:
        if checkpoint_id not in self._checkpoints:
            raise KeyError(f"Checkpoint {checkpoint_id} not found")
        compressed = self._checkpoints[checkpoint_id]
        decompressed = gzip.decompress(compressed)
        return json.loads(decompressed.decode("utf-8"))

    def export_snapshot_base64(self, checkpoint_id: str) -> str:
        if checkpoint_id not in self._checkpoints:
            raise KeyError(f"Checkpoint {checkpoint_id} not found")
        return base64.b64encode(self._checkpoints[checkpoint_id]).decode("ascii")

    def import_snapshot_base64(self, checkpoint_id: str, b64_str: str):
        self._checkpoints[checkpoint_id] = base64.b64decode(b64_str.encode("ascii"))
