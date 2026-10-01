"""Read-only documentary verification; no research imports or metric computation."""
import csv
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]


def relocations():
    with (ROOT / "docs/reproducibility/ARTIFACT_RELOCATIONS.csv").open(encoding="utf-8", newline="") as handle:
        return {row["old_path"]: row for row in csv.DictReader(handle)}


def canonical(name):
    name = name.replace("\\", "/")
    row = relocations().get(name)
    return row["new_path"] if row else name


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def markdown_links(path):
    text = path.read_text(encoding="utf-8-sig")
    text = re.sub(r"(?ms)^\s*(`{3,}|~{3,}).*?^\s*\1\s*$", "", text)
    definitions = dict(re.findall(r"(?m)^\s*\[([^\]]+)\]:\s*<?([^\s>]+)>?", text))
    targets = re.findall(r"!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)", text)
    for label, key in re.findall(r"\[([^\]\n]+)\]\[([^\]\n]*)\]", text):
        targets.append(definitions.get(key or label, "MISSING_REFERENCE:" + (key or label)))
    for label in re.findall(r"(?<!!)\[([^\]\n]+)\](?![(:\[])", text):
        if label in definitions:
            targets.append(definitions[label])
    targets += re.findall(r"<(?:a|img)\b[^>]*(?:href|src)=[\"']([^\"']+)", text, re.I)
    return [t.strip("<>") for t in targets]


def anchors(path):
    text = path.read_text(encoding="utf-8-sig")
    found = set(re.findall(r"\bid=[\"']([^\"']+)", text))
    counts = {}
    for title in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*#*\s*$", text):
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        n = counts.get(slug, 0)
        found.add(slug + ("-" + str(n) if n else ""))
        counts[slug] = n + 1
    return found


def exact_path_case(path):
    """Check spelling even on case-insensitive Windows filesystems."""
    path = Path(os.path.abspath(path))
    if not path.is_relative_to(ROOT):
        return True
    current = ROOT
    for part in path.relative_to(ROOT).parts:
        if not current.is_dir() or part not in {p.name for p in current.iterdir()}:
            return False
        current /= part
    return True


def check_links(excluded_paths=None):
    excluded_paths = set(excluded_paths or ())
    checked, broken = [], []
    paths = sorted(ROOT.glob("*.md"))
    for folder in ("docs", "results", "experiments", "scripts", "archive"):
        paths.extend(sorted((ROOT / folder).rglob("*.md")))
    for path in paths:
        if path.relative_to(ROOT).as_posix() in excluded_paths:
            continue
        for target in markdown_links(path):
            if target.startswith("MISSING_REFERENCE:"):
                broken.append({"path": path.relative_to(ROOT).as_posix(), "type": "undefined reference"})
                continue
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            dest = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            record = {"path": path.relative_to(ROOT).as_posix(), "target": target}
            checked.append(record)
            removed = dest.is_relative_to(ROOT) and dest.relative_to(ROOT).as_posix() in excluded_paths
            if not dest.exists() or removed:
                broken.append(dict(record, type="missing path"))
            elif not exact_path_case(path.parent / unquote(parsed.path) if parsed.path else path):
                broken.append(dict(record, type="path capitalization mismatch"))
            elif parsed.fragment and dest.suffix.lower() == ".md" and unquote(parsed.fragment) not in anchors(dest):
                broken.append(dict(record, type="missing anchor"))
    return {"documents": sum(p.relative_to(ROOT).as_posix() not in excluded_paths for p in paths),
            "checked": len(checked), "broken": broken}


def verify(excluded_paths=None):
    excluded_paths = set(excluded_paths or ())
    errors = []
    warnings = []
    # This approved snapshot fixes the 26-file scope. The 778-file import ledger
    # remains history; it is not an instruction to require removed copies.
    with (ROOT / "docs/reproducibility/APPROVED_REFERENCE_VERIFICATION.csv").open(encoding="utf-8", newline="") as handle:
        approved = {r["path"]: r for r in csv.DictReader(handle)}
    with (ROOT / "docs/reproducibility/initial_inventory.csv").open(encoding="utf-8", newline="") as handle:
        figures = {canonical(r["path"]): r for r in csv.DictReader(handle)
                   if r["path"].startswith("results/final_figures_v1/")}
    expected = {**approved, **figures}
    if len(approved) != 26 or len(figures) != 11:
        errors.append({"type": "approved scope must be 26 reference documents plus 11 original figure artifacts"})
    for name, row in expected.items():
        path = ROOT / name
        if name in excluded_paths or not path.is_file() or path.stat().st_size != int(row["size"]) or sha(path) != row["sha256"]:
            errors.append({"path": name, "type": "approved evidence checksum mismatch or missing file"})
    evidence_folders = ("experiments/final_spec", "results/final/phase11a", "results/final/phase11b")
    bundled = {p.relative_to(ROOT).as_posix() for folder in evidence_folders
               for p in (ROOT / folder).rglob("*") if p.is_file()
               and p.name != "README.md"
               and p.relative_to(ROOT).as_posix() not in excluded_paths}
    for name in sorted(bundled - set(approved)):
        errors.append({"path": name, "type": "outside approved reference scope"})
    manifest = ROOT / "docs/reproducibility/final_artifacts.csv"
    if manifest.exists():
        with manifest.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
            if len(rows) != 37 or {r["path"] for r in rows} != set(expected):
                errors.append({"type": "active artifact manifest differs from approved 37-file scope"})
            for row in rows:
                path = ROOT / row["path"]
                if row["path"] in excluded_paths or not path.is_file() or sha(path) != row["sha256"]:
                    errors.append({"path": row["path"], "type": "artifact checksum mismatch"})
    else:
        errors.append({"path": "docs/reproducibility/final_artifacts.csv", "type": "missing manifest"})
    provenance = json.loads((ROOT / "results/figures/provenance.json").read_text())
    for name, expected in provenance["input_sha256"].items():
        path = ROOT / canonical(name)
        if path.relative_to(ROOT).as_posix() in excluded_paths or not path.exists() or sha(path) != expected:
            errors.append({"path": path.relative_to(ROOT).as_posix(), "type": "figure input checksum mismatch"})
    plotter = ROOT / "scripts/plot_final_five_seed.py"
    if sha(plotter) != provenance["source_sha256"]:
        normalized = hashlib.sha256(plotter.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        if normalized == provenance["source_sha256"]:
            warnings.append({"path": "scripts/plot_final_five_seed.py",
                             "type": "working-tree byte hash differs; LF-normalized source matches recorded figure provenance"})
        else:
            errors.append({"path": "scripts/plot_final_five_seed.py", "type": "figure source checksum mismatch"})
    # Frozen CSV/JSON provenance keeps original path values. Resolve locations
    # through the relocation ledger, while checking exact content bytes.
    moved = relocations()
    for old, row in moved.items():
        path = ROOT / row["new_path"]
        if (ROOT / old).exists() or not path.is_file() or sha(path) != row["sha256"]:
            errors.append({"path": row["new_path"], "type": "relocated content mismatch, missing file, or old duplicate"})
    baseline_path = ROOT / "docs/reproducibility/STRUCTURAL_SIMPLIFICATION_BASELINE.json"
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    for old, digest in baseline.items():
        path = ROOT / canonical(old)
        if not path.is_file() or sha(path) != digest:
            errors.append({"path": canonical(old), "type": "protected content changed"})
    links = check_links(excluded_paths)
    errors += links["broken"]
    return {"approved_reference_documents": len(approved), "original_figure_artifacts": len(figures),
            "simulated_removals": len(excluded_paths),
            "relocated_files": len(moved), "protected_files": len(baseline),
            "figure_inputs": len(provenance["input_sha256"]), "links": links,
            "errors": errors, "warnings": warnings, "status": "PASS" if not errors else "FAIL",
            "scope": "Documentary integrity only; no predictions or metrics recalculated."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-removals", type=Path, help="Read a path-column CSV and verify as if those files were absent; deletes nothing")
    args = parser.parse_args()
    excluded = set()
    if args.preview_removals:
        with args.preview_removals.open(encoding="utf-8", newline="") as handle:
            excluded = {row["path"] for row in csv.DictReader(handle)}
    result = verify(excluded)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
