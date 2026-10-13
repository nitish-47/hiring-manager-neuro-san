import asyncio
from pathlib import Path
from typing import Any

from neuro_san.interfaces.coded_tool import CodedTool


class ProjectReadTool(CodedTool):
    """Reads a UTF-8 text file inside the current project."""

    async def async_invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> str:
        relative_path: str = str(args.get("path", "")).strip()
        max_chars: int = int(args.get("max_chars", 50000))
        if not relative_path:
            return "Error: 'path' is required."
        try:
            return await asyncio.to_thread(self._read, relative_path, max_chars)
        except (OSError, UnicodeError, ValueError) as exc:
            return f"Error: could not read {relative_path}: {exc}"

    def _read(self, relative_path: str, max_chars: int) -> str:
        root: Path = Path.cwd().resolve()
        target: Path = (root / relative_path).resolve()
        if not target.is_relative_to(root):
            raise ValueError("path resolves outside the current project")
        if not target.is_file():
            raise ValueError("file does not exist")
        content: str = target.read_text(encoding="utf-8")
        if max_chars > 0 and len(content) > max_chars:
            return content[:max_chars] + "\n...<truncated>"
        return content
