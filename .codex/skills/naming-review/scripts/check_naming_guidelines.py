#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


SOURCE_SUFFIXES = {
    ".cs",
    ".dart",
    ".go",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".kts",
    ".php",
    ".py",
    ".rb",
    ".scala",
    ".swift",
    ".ts",
    ".tsx",
}

SKIP_DIRS = {
    ".git",
    ".idea",
    ".next",
    ".venv",
    "bin",
    "build",
    "dist",
    "node_modules",
    "obj",
    "out",
    "target",
}

ABBREVIATIONS = {
    "calc": "Calculate",
    "exec": "Execute",
    "proc": "Process",
    "msg": "Message",
    "info": "Information",
    "num": "Number",
    "str": "String",
    "ctx": "Context",
    "repo": "Repository",
    "auth": "Authentication",
    "config": "Configuration",
    "env": "Environment",
}

AMBIGUOUS_STANDALONE = {
    "common",
    "helper",
    "util",
    "data",
    "info",
    "object",
    "item",
    "task",
    "thing",
    "stuff",
}

AMBIGUOUS_FUNCTION_PREFIXES = {
    "do": "Create / Update / Delete など具体的な動詞に置き換える",
    "process": "ConvertTo / Filter / ExecuteBatch など具体的な動詞に置き換える",
    "manage": "管理対象を含む具体名にする",
    "run": "Start / ExecuteJob など具体的な動詞に置き換える",
    "check": "Exists / Is / Has / Detect など意図に応じて使い分ける",
    "build": "Builder パターン以外では Create / Generate / Compose / ConvertTo などに置き換える",
}

NAME_PATTERNS = [
    ("function", re.compile(r"^\s*(?:async\s+)?def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")),
    ("function", re.compile(r"^\s*function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")),
    ("function", re.compile(r"^\s*fun\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")),
    (
        "function",
        re.compile(
            r"^\s*(?:(?:public|private|protected|internal|static|virtual|override|final|abstract|sealed|async)\s+)*(?:[A-Za-z_][A-Za-z0-9_<>\[\],?]*\s+)+([A-Za-z_][A-Za-z0-9_]*)\s*\("
        ),
    ),
    ("type", re.compile(r"^\s*(?:class|interface|enum|record|struct|type)\s+([A-Za-z_][A-Za-z0-9_]*)\b")),
    ("variable", re.compile(r"^\s*(?:const|let|var|final)\s+([A-Za-z_][A-Za-z0-9_]*)\b")),
    ("variable", re.compile(r"^\s*(?:self|this)\.([A-Za-z_][A-Za-z0-9_]*)\s*=")),
    ("variable", re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*")),
]


@dataclass(frozen=True)
class Finding:
    severity: str
    category: str
    path: str
    line: int | None
    name: str
    message: str
    suggestion: str | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check repository names against the shared naming guidelines."
    )
    parser.add_argument("paths", nargs="*", default=["."])
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--max-findings", type=int, default=200)
    return parser.parse_args()


def split_identifier_parts(name: str) -> list[str]:
    normalized = name.replace("-", "_")
    parts: list[str] = []
    for chunk in normalized.split("_"):
        if not chunk:
            continue
        parts.extend(
            part
            for part in re.findall(r"[A-Z]+(?=[A-Z][a-z]|\d|$)|[A-Z]?[a-z]+|\d+", chunk)
            if part
        )
    return parts or [name]


def should_skip_dir(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def iter_source_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_file():
            if path.suffix in SOURCE_SUFFIXES:
                files.append(path)
            continue

        if not path.exists():
            continue

        for candidate in path.rglob("*"):
            if candidate.is_dir() and should_skip_dir(candidate):
                continue
            if candidate.is_file() and candidate.suffix in SOURCE_SUFFIXES and not should_skip_dir(candidate):
                files.append(candidate)
    return sorted(set(files))


def add_finding(
    findings: list[Finding],
    severity: str,
    category: str,
    path: Path,
    line: int | None,
    name: str,
    message: str,
    suggestion: str | None = None,
) -> None:
    findings.append(
        Finding(
            severity=severity,
            category=category,
            path=str(path),
            line=line,
            name=name,
            message=message,
            suggestion=suggestion,
        )
    )


def collect_token_findings(
    findings: list[Finding],
    path: Path,
    line_number: int | None,
    name: str,
) -> None:
    parts = [part.lower() for part in split_identifier_parts(name)]
    if not parts:
        return

    for part in parts:
        replacement = ABBREVIATIONS.get(part)
        if replacement is None:
            continue
        add_finding(
            findings,
            "error",
            "abbreviation",
            path,
            line_number,
            name,
            f"`{part}` は禁止略語です。",
            f"`{replacement}` を使う",
        )

    if len(parts) == 1 and parts[0] in AMBIGUOUS_STANDALONE:
        add_finding(
            findings,
            "warning",
            "ambiguous-name",
            path,
            line_number,
            name,
            f"`{name}` は対象や責務が曖昧です。",
            "対象や責務が分かる具体名にする",
        )


def collect_path_name_findings(path: Path, findings: list[Finding]) -> None:
    for part in path.parts:
        if part in {".", ""}:
            continue
        stem = Path(part).stem if "." in part else part
        collect_token_findings(findings, path, None, stem)


def collect_function_name_findings(
    path: Path, line_number: int, name: str, findings: list[Finding]
) -> None:
    parts = [part.lower() for part in split_identifier_parts(name)]
    if not parts:
        return

    first = parts[0]
    if first in AMBIGUOUS_FUNCTION_PREFIXES:
        if first == "build" and "builder" in parts:
            return
        add_finding(
            findings,
            "warning",
            "ambiguous-verb",
            path,
            line_number,
            name,
            f"`{first}` はこの命名規則では曖昧な動詞です。",
            AMBIGUOUS_FUNCTION_PREFIXES[first],
        )

    if name.startswith("Async") or ("Async" in name and not name.endswith("Async")):
        add_finding(
            findings,
            "error",
            "async-suffix",
            path,
            line_number,
            name,
            "`Async` は接尾辞で統一する必要があります。",
            "末尾だけを `Async` にする",
        )

    if name.startswith("AbleTo"):
        add_finding(
            findings,
            "warning",
            "bool-prefix",
            path,
            line_number,
            name,
            "`AbleTo` ではなく `Can` を使う規則です。",
            f"`Can{name.removeprefix('AbleTo')}` を検討する",
        )

    if name.startswith("Need"):
        add_finding(
            findings,
            "warning",
            "bool-prefix",
            path,
            line_number,
            name,
            "`Need` ではなく `Should` を使う規則です。",
            f"`Should{name.removeprefix('Need')}` を検討する",
        )


def collect_file_findings(path: Path, findings: list[Finding]) -> None:
    collect_path_name_findings(path, findings)

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = path.read_text(encoding="utf-8", errors="ignore")

    seen_identifiers: set[tuple[int, str, str]] = set()

    for line_number, line in enumerate(content.splitlines(), start=1):
        for kind, pattern in NAME_PATTERNS:
            match = pattern.match(line)
            if match is None:
                continue

            identifier = match.group(1)
            key = (line_number, kind, identifier)
            if key in seen_identifiers:
                continue
            seen_identifiers.add(key)

            collect_token_findings(findings, path, line_number, identifier)
            if kind == "function":
                collect_function_name_findings(path, line_number, identifier, findings)


def main() -> int:
    args = parse_args()
    findings: list[Finding] = []

    for path in iter_source_files(args.paths):
        collect_file_findings(path, findings)
        if len(findings) >= args.max_findings:
            break

    findings = findings[: args.max_findings]

    if args.as_json:
        print(json.dumps([asdict(finding) for finding in findings], ensure_ascii=False, indent=2))
        return 0

    if not findings:
        print("No naming guideline findings.")
        return 0

    for finding in findings:
        location = f"{finding.path}:{finding.line}" if finding.line is not None else finding.path
        suffix = f" Suggestion: {finding.suggestion}" if finding.suggestion else ""
        print(
            f"{location}: [{finding.severity}] {finding.category} `{finding.name}` - {finding.message}{suffix}"
        )

    print(f"\nTotal findings: {len(findings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
