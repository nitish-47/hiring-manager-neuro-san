import asyncio
import json
import os
from pathlib import Path
from typing import Any

from neuro_san.interfaces.coded_tool import CodedTool


class ToolboxSearchTool(CodedTool):
    """Searches known toolbox definition files for reusable capabilities."""

    async def async_invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> str:
        query: str = str(args.get("query", "")).strip()
        if not query:
            return "Error: 'query' is required."
        return await asyncio.to_thread(self._search, query)

    def _search(self, query: str) -> str:
        root: Path = Path.cwd().resolve()
        candidates: list[Path] = []
        configured: str = os.environ.get("AGENT_TOOLBOX_INFO_FILE", "")
        for raw_path in configured.split(os.pathsep):
            if raw_path:
                candidates.append(Path(raw_path))
        candidates.extend(
            [
                root / "toolbox_info.hocon",
                root / "config" / "toolbox_info.hocon",
                root / "neuro_san_studio" / "toolbox" / "toolbox_info.hocon",
            ]
        )
        for path in root.rglob("toolbox_info.hocon"):
            candidates.append(path)

        needle: str = query.casefold()
        seen: set[str] = set()
        matches: list[dict[str, Any]] = []
        for candidate in candidates:
            try:
                resolved: Path = candidate.expanduser().resolve()
            except OSError:
                continue
            key: str = str(resolved)
            if key in seen or not resolved.is_file():
                continue
            seen.add(key)
            try:
                lines: list[str] = resolved.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeError):
                continue
            for index, line in enumerate(lines):
                if needle in line.casefold():
                    start: int = max(0, index - 2)
                    end: int = min(len(lines), index + 3)
                    matches.append(
                        {"file": key, "line": index + 1, "context": "\n".join(lines[start:end])}
                    )
                    if len(matches) >= 30:
                        return json.dumps({"query": query, "matches": matches}, indent=2)
        return json.dumps({"query": query, "matches": matches}, indent=2)
