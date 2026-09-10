#!/usr/bin/env python3
"""Rename the starter package and update common references.

Usage:
    python scripts/rename_package.py new_package_name
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_NAME = "mypackage"
EXCLUDE_DIRS = {".git", "envs", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
TEXT_EXTENSIONS = {".py", ".md", ".toml", ".yml", ".yaml", ".ipynb", ".txt", ".ini"}


def validate_package_name(name: str) -> None:
    if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
        raise ValueError(
            "Package name must match [a-z][a-z0-9_]* (lowercase, digits, underscore)."
        )


def iter_text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS:
            files.append(path)
    return files


def replace_text_refs(old_name: str, new_name: str) -> int:
    updated = 0
    for file_path in iter_text_files(ROOT):
        text = file_path.read_text(encoding="utf-8")
        new_text = text.replace(old_name, new_name)
        if new_text != text:
            file_path.write_text(new_text, encoding="utf-8")
            updated += 1
    return updated


def rename_package_dir(old_name: str, new_name: str) -> bool:
    old_dir = ROOT / old_name
    new_dir = ROOT / new_name
    if not old_dir.exists():
        return False
    if new_dir.exists():
        raise FileExistsError(f"Target package directory already exists: {new_dir}")
    old_dir.rename(new_dir)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Rename starter package and update references")
    parser.add_argument("new_name", help="New package name, e.g. soil_analysis")
    args = parser.parse_args()

    new_name = args.new_name.strip()
    validate_package_name(new_name)

    if new_name == OLD_NAME:
        print("Package name is already 'mypackage'; no changes made.")
        return

    renamed = rename_package_dir(OLD_NAME, new_name)
    updated_files = replace_text_refs(OLD_NAME, new_name)

    if renamed:
        print(f"Renamed package folder: {OLD_NAME} -> {new_name}")
    else:
        print(f"Package folder '{OLD_NAME}' not found. Applied text updates only.")

    print(f"Updated references in {updated_files} files.")
    print("Done. Next step: run `make test` to verify the rename.")


if __name__ == "__main__":
    main()
