import subprocess
from pathlib import Path
from typing import Generator

from haystack.types import SearchResult


def find_plus_context(
    term: str, start_dir: Path, context_lines: int
) -> Generator[SearchResult, None, None]:
    """Generator that yields each ripgrep result with its context one at a time"""
    rg_command = ["rg", "-C", str(context_lines), term]
    cmd_str = subprocess.list2cmdline(rg_command)
    print(f"Executing ripgrep command: {cmd_str}")

    try:
        process = subprocess.Popen(
            rg_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=start_dir,
        )

        if process.stdout is None:
            return

        buffer: list[str] = []
        current_file: str | None = None

        for line in process.stdout:
            if line.startswith("--"):
                if buffer and current_file:
                    yield SearchResult(filename=current_file, lines=buffer.copy())
                    buffer.clear()
                    current_file = None
            else:
                # Parse the filename and content
                parts = line.split(":", 1)
                # print(parts)
                if len(parts) >= 2:
                    if not current_file:
                        current_file = parts[0]
                buffer.append(line.rstrip())

        if buffer and current_file:
            yield SearchResult(filename=current_file, lines=buffer.copy())

        process.wait()
        if (
            process.returncode != 0 and process.returncode != 1
        ):  # 1 means no matches, which is ok
            if process.stderr is not None:
                stderr = process.stderr.read()
                raise subprocess.CalledProcessError(
                    process.returncode, rg_command, stderr
                )

    except subprocess.CalledProcessError as e:
        print(f"Error executing ripgrep: {e}")
        return
