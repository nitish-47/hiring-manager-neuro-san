import asyncio
import json
from pathlib import Path
from typing import Any

from neuro_san.interfaces.coded_tool import CodedTool


class ProjectInspectTool(CodedTool):
    """Inspects Neuro SAN-relevant files in the current project."""

    async def async_invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> str:
        max_depth: int = int(args.get("max_depth", 4))
        return await asyncio.to_thread(self._inspect, max_depth)

    def _inspect(self, max_depth: int) -> str:
        root: Path = Path.cwd().resolve()
        interesting_roots: tuple[str, ...] = (
            "registries", "coded_tools", "middleware", "config", "mcp", "tests", "docs",
        )
        files: list[str] = []
        for root_name in interesting_roots:
            base: Path = root / root_name
            if not base.exists():
                continue
            for path in base.rglob("*"):
                if not path.is_file():
                    continue
                relative: Path = path.relative_to(root)
                if len(relative.parts) - 1 <= max_depth:
                    files.append(relative.as_posix())
        files.sort()
        return json.dumps(
            {
                "project_root": str(root),
                "files": files,
                "manifest_exists": (root / "registries" / "manifest.hocon").is_file(),
                "generated_manifest_exists": (root / "registries" / "generated" / "manifest.hocon").is_file(),
            },
            indent=2,
        )
