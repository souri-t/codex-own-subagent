#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

try:
    import lizard
except ImportError:  # pragma: no cover - handled at runtime
    lizard = None


SUPPORTED_EXTENSIONS = {
    ".cs": "csharp",
    ".java": "java",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".py": "python",
}

DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".idea",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    ".gradle",
    "bin",
    "build",
    "dist",
    "node_modules",
    "obj",
    "out",
    "target",
    "__pycache__",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze cyclomatic complexity for C#, Kotlin, Java, and Python via Lizard."
    )
    parser.add_argument("paths", nargs="*", default=["."], help="Files or directories to analyze.")
    parser.add_argument(
        "--mode",
        choices=("full", "diff"),
        default="full",
        help="Analyze the full target set or only files changed from a git ref.",
    )
    parser.add_argument(
        "--git-ref",
        default="origin/main",
        help="Git ref for diff mode. Uses '<git-ref>...HEAD'.",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=10,
        help="Report functions whose complexity is greater than or equal to this value.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Maximum number of hotspot functions to display.",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        help="Optional JSON output path.",
    )
    parser.add_argument(
        "--markdown-out",
        type=Path,
        help="Optional Markdown report output path.",
    )
    parser.add_argument(
        "--csv-out-dir",
        type=Path,
        help="Optional output directory for CSV tables.",
    )
    parser.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        help="Directory name to exclude. Can be specified multiple times.",
    )
    return parser.parse_args()


def ensure_lizard() -> None:
    if lizard is None:
        print(
            "lizard is not installed. Run 'python3 -m pip install lizard' first.",
            file=sys.stderr,
        )
        raise SystemExit(2)


def normalize_path(path: str | Path) -> Path:
    return Path(path).resolve()


def should_skip(path: Path, excluded_dirs: set[str]) -> bool:
    return any(part in excluded_dirs for part in path.parts)


def discover_files(paths: Iterable[str], excluded_dirs: set[str]) -> list[Path]:
    files: list[Path] = []
    for raw_path in paths:
        path = normalize_path(raw_path)
        if not path.exists():
            continue
        if path.is_file():
            if path.suffix.lower() in SUPPORTED_EXTENSIONS and not should_skip(path, excluded_dirs):
                files.append(path)
            continue

        for candidate in path.rglob("*"):
            if not candidate.is_file():
                continue
            if candidate.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            if should_skip(candidate, excluded_dirs):
                continue
            files.append(candidate.resolve())
    return sorted(set(files))


def git_diff_files(git_ref: str, excluded_dirs: set[str]) -> list[Path]:
    command = [
        "git",
        "diff",
        "--name-only",
        "--diff-filter=ACMR",
        f"{git_ref}...HEAD",
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        print(result.stderr.strip() or "Failed to collect git diff files.", file=sys.stderr)
        raise SystemExit(result.returncode)

    files: list[Path] = []
    for line in result.stdout.splitlines():
        path = normalize_path(line)
        if not path.exists():
            continue
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        if should_skip(path, excluded_dirs):
            continue
        files.append(path)
    return sorted(set(files))


def relative_to_cwd(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def classify_severity(score: int) -> str:
    if score >= 21:
        return "critical"
    if score >= 16:
        return "high"
    if score >= 11:
        return "medium"
    return "low"


def analyze_file(path: Path) -> list[dict]:
    analysis = lizard.analyze_file(str(path))
    entries: list[dict] = []
    for function in analysis.function_list:
        complexity = int(function.cyclomatic_complexity)
        entries.append(
            {
                "language": SUPPORTED_EXTENSIONS[path.suffix.lower()],
                "tool": "lizard",
                "file": relative_to_cwd(path),
                "symbol": function.long_name,
                "name": function.name,
                "start_line": int(function.start_line),
                "end_line": int(getattr(function, "end_line", function.start_line)),
                "nloc": int(function.nloc),
                "token_count": int(function.token_count),
                "parameter_count": int(function.parameter_count),
                "cyclomatic_complexity": complexity,
                "severity": classify_severity(complexity),
            }
        )
    return entries


def summarize(results: list[dict], threshold: int, top: int) -> str:
    total_functions = len(results)
    over_threshold = [entry for entry in results if entry["cyclomatic_complexity"] >= threshold]
    hotspots = sorted(
        results,
        key=lambda item: (item["cyclomatic_complexity"], item["nloc"], item["token_count"]),
        reverse=True,
    )[:top]

    by_language = Counter(entry["language"] for entry in results)

    lines = [
        "Cyclomatic Complexity Report",
        f"Functions analyzed: {total_functions}",
        f"Threshold: {threshold}",
        f"Threshold hits: {len(over_threshold)}",
        "Language summary: "
        + ", ".join(f"{language}={count}" for language, count in sorted(by_language.items())),
        "",
        f"Top {len(hotspots)} hotspots:",
    ]

    for index, entry in enumerate(hotspots, start=1):
        lines.append(
            (
                f"{index}. CC={entry['cyclomatic_complexity']} "
                f"[{entry['severity']}] {entry['symbol']} "
                f"({entry['file']}:{entry['start_line']})"
            )
        )

    if over_threshold:
        lines.append("")
        lines.append(f"Functions with CC >= {threshold}:")
        for entry in sorted(
            over_threshold,
            key=lambda item: (item["cyclomatic_complexity"], item["file"], item["start_line"]),
            reverse=True,
        ):
            lines.append(
                (
                    f"- CC={entry['cyclomatic_complexity']} "
                    f"{entry['symbol']} ({entry['file']}:{entry['start_line']})"
                )
            )

    return "\n".join(lines)


def format_markdown_table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(rows[0]) + " |"
    separator = "| " + " | ".join("---" for _ in rows[0]) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows[1:]]
    return "\n".join([header, separator, *body])


def top_hotspots(results: list[dict], limit: int) -> list[dict]:
    return sorted(
        results,
        key=lambda item: (item["cyclomatic_complexity"], item["nloc"], item["token_count"]),
        reverse=True,
    )[:limit]


def threshold_hits(results: list[dict], threshold: int) -> list[dict]:
    return sorted(
        [entry for entry in results if entry["cyclomatic_complexity"] >= threshold],
        key=lambda item: (item["cyclomatic_complexity"], item["file"], item["start_line"]),
        reverse=True,
    )


def build_markdown_report(
    *,
    results: list[dict],
    files: list[Path],
    mode: str,
    git_ref: str | None,
    threshold: int,
    top: int,
) -> str:
    hits = threshold_hits(results, threshold)
    hotspots = top_hotspots(results, top)
    language_counts = Counter(entry["language"] for entry in results)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "# Cyclomatic Complexity Report",
        "",
        "## Summary",
        "",
        format_markdown_table(
            [
                ["Item", "Value"],
                ["Generated At", generated_at],
                ["Mode", mode],
                ["Git Ref", git_ref or "-"],
                ["Files Analyzed", str(len(files))],
                ["Functions Analyzed", str(len(results))],
                ["Threshold", str(threshold)],
                ["Threshold Hits", str(len(hits))],
                ["Languages", ", ".join(f"{lang}={count}" for lang, count in sorted(language_counts.items())) or "-"],
            ]
        ),
        "",
        "## Top Hotspots",
        "",
    ]

    if hotspots:
        lines.extend(
            [
                format_markdown_table(
                    [
                        ["Rank", "CC", "Severity", "Language", "Symbol", "File", "Line", "NLOC", "Params"],
                        *[
                            [
                                str(index),
                                str(entry["cyclomatic_complexity"]),
                                entry["severity"],
                                entry["language"],
                                f"`{entry['symbol']}`",
                                f"`{entry['file']}`",
                                str(entry["start_line"]),
                                str(entry["nloc"]),
                                str(entry["parameter_count"]),
                            ]
                            for index, entry in enumerate(hotspots, start=1)
                        ],
                    ]
                ),
                "",
            ]
        )
    else:
        lines.extend(["No functions were analyzed.", ""])

    lines.extend(["## Threshold Hits", ""])
    if hits:
        lines.extend(
            [
                format_markdown_table(
                    [
                        ["CC", "Severity", "Language", "Symbol", "File", "Line", "NLOC", "Tokens"],
                        *[
                            [
                                str(entry["cyclomatic_complexity"]),
                                entry["severity"],
                                entry["language"],
                                f"`{entry['symbol']}`",
                                f"`{entry['file']}`",
                                str(entry["start_line"]),
                                str(entry["nloc"]),
                                str(entry["token_count"]),
                            ]
                            for entry in hits
                        ],
                    ]
                ),
                "",
            ]
        )
    else:
        lines.extend([f"No functions exceeded the threshold ({threshold}).", ""])

    lines.extend(["## Files Analyzed", ""])
    lines.extend([f"- `{relative_to_cwd(path)}`" for path in files])
    lines.append("")
    return "\n".join(lines)


def write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def write_csv_reports(
    *,
    output_dir: Path,
    results: list[dict],
    files: list[Path],
    mode: str,
    git_ref: str | None,
    threshold: int,
    top: int,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    hits = threshold_hits(results, threshold)
    hotspots = top_hotspots(results, top)
    language_counts = Counter(entry["language"] for entry in results)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    summary_path = output_dir / "summary.csv"
    write_csv(
        summary_path,
        ["item", "value"],
        [
            ["generated_at", generated_at],
            ["mode", mode],
            ["git_ref", git_ref or "-"],
            ["files_analyzed", str(len(files))],
            ["functions_analyzed", str(len(results))],
            ["threshold", str(threshold)],
            ["threshold_hits", str(len(hits))],
            ["languages", ", ".join(f"{lang}={count}" for lang, count in sorted(language_counts.items())) or "-"],
        ],
    )

    hotspots_path = output_dir / "top_hotspots.csv"
    write_csv(
        hotspots_path,
        ["rank", "cc", "severity", "language", "symbol", "file", "line", "nloc", "params"],
        [
            [
                str(index),
                str(entry["cyclomatic_complexity"]),
                entry["severity"],
                entry["language"],
                entry["symbol"],
                entry["file"],
                str(entry["start_line"]),
                str(entry["nloc"]),
                str(entry["parameter_count"]),
            ]
            for index, entry in enumerate(hotspots, start=1)
        ],
    )

    threshold_hits_path = output_dir / "threshold_hits.csv"
    write_csv(
        threshold_hits_path,
        ["cc", "severity", "language", "symbol", "file", "line", "nloc", "tokens"],
        [
            [
                str(entry["cyclomatic_complexity"]),
                entry["severity"],
                entry["language"],
                entry["symbol"],
                entry["file"],
                str(entry["start_line"]),
                str(entry["nloc"]),
                str(entry["token_count"]),
            ]
            for entry in hits
        ],
    )

    return [summary_path, hotspots_path, threshold_hits_path]


def main() -> int:
    args = parse_args()
    ensure_lizard()

    excluded_dirs = DEFAULT_EXCLUDE_DIRS | set(args.exclude_dir)
    if args.mode == "diff":
        files = git_diff_files(args.git_ref, excluded_dirs)
    else:
        files = discover_files(args.paths, excluded_dirs)

    if not files:
        print("No supported files found.")
        return 0

    results: list[dict] = []
    for path in files:
        results.extend(analyze_file(path))

    report = {
        "tool": "lizard",
        "mode": args.mode,
        "git_ref": args.git_ref if args.mode == "diff" else None,
        "threshold": args.threshold,
        "files_analyzed": [relative_to_cwd(path) for path in files],
        "results": results,
    }

    print(summarize(results, args.threshold, args.top))

    if args.json_out:
        args.json_out.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"\nJSON report written to {args.json_out}")

    if args.markdown_out:
        args.markdown_out.write_text(
            build_markdown_report(
                results=results,
                files=files,
                mode=args.mode,
                git_ref=args.git_ref if args.mode == "diff" else None,
                threshold=args.threshold,
                top=args.top,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"Markdown report written to {args.markdown_out}")

    if args.csv_out_dir:
        csv_paths = write_csv_reports(
            output_dir=args.csv_out_dir,
            results=results,
            files=files,
            mode=args.mode,
            git_ref=args.git_ref if args.mode == "diff" else None,
            threshold=args.threshold,
            top=args.top,
        )
        print("CSV tables written to:")
        for path in csv_paths:
            print(f"- {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
