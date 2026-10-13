import asyncio
import os
from pathlib import Path
from typing import Any
from uuid import uuid4

from neuro_san.interfaces.coded_tool import CodedTool


class ManifestUpdateTool(CodedTool):
    """Adds or updates an entry in the generated Neuro SAN manifest."""

    async def async_invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> str:
        network_path: str = str(args.get("network_path", "")).strip().replace("\\", "/")
        manifest_path: str = str(args.get("manifest_path", "registries/generated/manifest.hocon")).strip()
        serve: bool = bool(args.get("serve", True))
        public_value: Any = args.get("public")
        if not network_path:
            return "Error: 'network_path' is required."
        try:
            return await asyncio.to_thread(self._update, manifest_path, network_path, serve, public_value)
        except (OSError, ValueError) as exc:
            return f"Error: could not update manifest: {exc}"

    def _update(self, manifest_path: str, network_path: str, serve: bool, public_value: Any) -> str:
        if not network_path.startswith("generated/") or not network_path.endswith(".hocon"):
            raise ValueError("network_path must match generated/<name>.hocon")
        root: Path = Path.cwd().resolve()
        target: Path = (root / manifest_path).resolve()
        generated_root: Path = (root / "registries" / "generated").resolve()
        if not target.is_relative_to(generated_root):
            raise ValueError("manifest must remain under registries/generated")
        target.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(public_value, bool):
            value: str = (
                '{ "serve": ' + str(serve).lower() + ', "public": ' + str(public_value).lower() + ' }'
            )
        else:
            value = str(serve).lower()
        entry: str = f'    "{network_path}": {value}'

        existing: str = target.read_text(encoding="utf-8") if target.exists() else "{\n}\n"
        lines: list[str] = existing.splitlines()
        updated: list[str] = []
        replaced: bool = False
        for line in lines:
            if f'"{network_path}"' in line:
                suffix: str = "," if line.rstrip().endswith(",") else ""
                updated.append(entry + suffix)
                replaced = True
            else:
                updated.append(line)

        if not replaced:
            close_index: int = -1
            for index in range(len(updated) - 1, -1, -1):
                if updated[index].strip() == "}":
                    close_index = index
                    break
            if close_index < 0:
                raise ValueError("generated manifest is not brace-delimited HOCON")
            previous_index: int = close_index - 1
            while previous_index >= 0 and not updated[previous_index].strip():
                previous_index -= 1
            if previous_index >= 0 and updated[previous_index].strip() != "{":
                if not updated[previous_index].rstrip().endswith(","):
                    updated[previous_index] = updated[previous_index].rstrip() + ","
            updated.insert(close_index, entry)

        output: str = "\n".join(updated).rstrip() + "\n"
        temp_path: Path = target.with_name(f".{target.name}.{uuid4().hex}.tmp")
        try:
            temp_path.write_text(output, encoding="utf-8", newline="\n")
            os.replace(temp_path, target)
        finally:
            if temp_path.exists():
                temp_path.unlink()
        action: str = "UPDATED" if replaced else "REGISTERED"
        return f"{action} {network_path} in {target.relative_to(root).as_posix()}"
