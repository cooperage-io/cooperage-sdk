"""Workspace helpers for Cooperage MCP servers."""

import os
from pathlib import Path


class Workspace:
    """Interface for the shared /workspace volume.

    Handles path resolution, traversal protection, and the
    COOPERAGE_WORKSPACE env var so server devs don't have to.
    """

    def __init__(self):
        self._root = Path(os.environ.get("COOPERAGE_WORKSPACE", "/workspace"))

    @property
    def root(self) -> Path:
        """The workspace root as a Path."""
        return self._root

    def path(self, path: str) -> Path:
        """Resolve a relative path within the workspace.

        Returns a full Path you can use with any library:

            data = workspace.path("input.csv").read_text()
            image = Image.open(workspace.path("photo.png"))
            df = pd.read_csv(workspace.path("data.csv"))
            plt.savefig(workspace.path("chart.png"))

        Raises ValueError on path traversal attempts.
        """
        full = (self._root / path).resolve()
        if not str(full).startswith(str(self._root.resolve())):
            raise ValueError(f"Path {path!r} escapes the workspace")
        return full

    def exists(self, path: str) -> bool:
        """Check if a file exists in the workspace."""
        return self.path(path).exists()

    def list(self, subdir: str = "") -> list[str]:
        """List files in the workspace (or a subdirectory), relative to root."""
        target = self.path(subdir) if subdir else self._root
        if not target.exists():
            return []
        return sorted(
            str(p.relative_to(self._root))
            for p in target.rglob("*")
            if p.is_file()
        )


workspace = Workspace()
