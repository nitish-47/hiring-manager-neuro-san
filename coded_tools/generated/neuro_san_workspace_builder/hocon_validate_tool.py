import asyncio
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from neuro_san.interfaces.coded_tool import CodedTool


class HoconValidateTool(CodedTool):
    """Runs Neuro SAN structural HOCON validation in the current project."""

    async def async_invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> str:
        relative_path: str = str(args.get("path", "")).strip()
        verbose: bool = bool(args.get("verbose", True))
        if not relative_path:
            return "Error: 'path' is required."
        try:
            return await asyncio.to_thread(self._validate, relative_path, verbose)
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            return f"Error: validation could not run: {exc}"

    def _validate(self, relative_path: str, verbose: bool) -> str:
        root: Path = Path.cwd().resolve()
        target: Path = (root / relative_path).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            raise ValueError("validation target must be an existing project file")

        ns_executable: str | None = shutil.which("ns")
        if ns_executable:
            command: list[str] = [ns_executable, "validate", relative_path]
            if verbose:
                command.append("--verbose")
        else:
            command = [sys.executable, "-m", "neuro_san.client.hocon_validator_cli", relative_path]
            if verbose:
                command.append("--verbose")

        completed: subprocess.CompletedProcess[str] = subprocess.run(
            command,
            cwd=root,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
        return json.dumps(
            {
                "path": relative_path,
                "exit_code": completed.returncode,
                "passed": completed.returncode == 0,
                "stdout": completed.stdout[-20000:],
                "stderr": completed.stderr[-20000:],
            },
            indent=2,
        )
