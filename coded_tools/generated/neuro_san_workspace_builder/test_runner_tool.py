import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from neuro_san.interfaces.coded_tool import CodedTool


class TestRunnerTool(CodedTool):
    """Runs a restricted pytest command in the current project."""

    async def async_invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> str:
        target: str = str(args.get("target", "")).strip()
        keyword: str = str(args.get("keyword", "")).strip()
        try:
            return await asyncio.to_thread(self._run, target, keyword)
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            return f"Error: tests could not run: {exc}"

    def _run(self, target: str, keyword: str) -> str:
        root: Path = Path.cwd().resolve()
        command: list[str] = [sys.executable, "-m", "pytest", "-q"]
        if target:
            resolved: Path = (root / target).resolve()
            if not resolved.is_relative_to(root):
                raise ValueError("pytest target resolves outside the current project")
            command.append(target)
        if keyword:
            command.extend(["-k", keyword])

        completed: subprocess.CompletedProcess[str] = subprocess.run(
            command,
            cwd=root,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )
        return json.dumps(
            {
                "exit_code": completed.returncode,
                "passed": completed.returncode == 0,
                "stdout": completed.stdout[-20000:],
                "stderr": completed.stderr[-20000:],
            },
            indent=2,
        )
