#!/usr/bin/env python3
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "MAYANK_DROID_Instaloader.zip"

EXCLUDE_DIRS = {".git", "__pycache__", ".mypy_cache", ".pytest_cache", ".venv", "build", "dist", "*.egg-info"}
EXCLUDE_NAMES = {OUT.name}

def excluded(path: Path) -> bool:
    if path.name in EXCLUDE_NAMES:
        return True
    return any(part == ".git" or part in {".venv", "__pycache__", ".mypy_cache", ".pytest_cache", "build", "dist"} or part.endswith(".egg-info")
               for part in path.relative_to(ROOT).parts)

files = [p for p in ROOT.rglob("*") if p.is_file() and not excluded(p)]
files.sort()

with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for path in files:
        zf.write(path, Path(ROOT.name) / path.relative_to(ROOT))

print(f"Created: {OUT}")
print(f"Files: {len(files)}")
print(f"Size: {OUT.stat().st_size:,} bytes")
