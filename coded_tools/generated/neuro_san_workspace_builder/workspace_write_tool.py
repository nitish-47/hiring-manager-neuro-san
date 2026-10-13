import asyncio
import os
from pathlib import Path
from typing import Any
from uuid import uuid4

from neuro_san.interfaces.coded_tool import CodedTool


class WorkspaceWriteTool(CodedTool):
    """Atomically writes generated text files inside approved project directories."""

    async def async_invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> str:
        relative_path: str = str(args.get("path", "")).strip()
        content: str = str(args.get("content", ""))
        overwrite: bool = bool(args.get("overwrite", True))
        raw_prefixes: Any = args.get("allowed_prefixes", [])
        allowed_prefixes: list[str] = [str(item) for item in raw_prefixes] if isinstance(raw_prefixes, list) else []
        if not relative_path:
            return "Error: 'path' is required."
        if not allowed_prefixes:
            return "Error: no allowed_prefixes configured for WorkspaceWriteTool."
        try:
            return await asyncio.to_thread(self._write, relative_path, content, overwrite, allowed_prefixes)
        except (OSError, ValueError) as exc:
            return f"Error: could not write {relative_path}: {exc}"

    def _write(self, relative_path: str, content: str, overwrite: bool, allowed_prefixes: list[str]) -> str:
        normalized: str = relative_path.replace("\\", "/").lstrip("/")
        if not any(normalized.startswith(prefix) for prefix in allowed_prefixes):
            raise ValueError(f"path is outside approved prefixes: {allowed_prefixes}")
        root: Path = Path.cwd().resolve()
        target: Path = (root / normalized).resolve()
        if not target.is_relative_to(root):
            raise ValueError("path resolves outside the current project")
        if target.exists() and not overwrite:
            raise ValueError("target already exists and overwrite=false")
        target.parent.mkdir(parents=True, exist_ok=True)
        temp_path: Path = target.with_name(f".{target.name}.{uuid4().hex}.tmp")
        try:
            temp_path.write_text(content, encoding="utf-8", newline="\n")
            os.replace(temp_path, target)
        finally:
            if temp_path.exists():
                temp_path.unlink()
        return f"WROTE {normalized} ({len(content.encode('utf-8'))} bytes)"
