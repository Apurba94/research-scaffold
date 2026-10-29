"""Project templates rendered with string.Template; never overwrites existing files."""
import datetime
import os
import re
import string

BASE_DIRS = ["data/raw", "data/interim", "data/processed", "docs", "notebooks", "results/figures",
             "results/tables", "src/$package", "tests"]
EXTRA_DIRS = {"ml": ["models", "configs", "results/runs"], "paper": ["manuscript/figures", "manuscript/sections"],
              "basic": []}

README = """# $title

$description

**Author:** $author$orcid_line
**Started:** $date

## Project structure

```
data/raw/          original, immutable data (never edit by hand)
data/interim/      intermediate transformed data
data/processed/    final datasets used for analysis
notebooks/         exploratory notebooks (named NN-initials-topic.ipynb)
src/$package/      reusable analysis code
results/figures/   generated figures (do not edit by hand)
results/tables/    generated tables
docs/              documentation, protocols, data dictionary
tests/             tests for src/
$extra_tree```

## Reproducing the results

1. Create the environment: `python -m venv .venv && pip install -r requirements.txt`
2. Put the raw data in `data/raw/` (see `docs/DATA.md` for sources and checksums)
3. Run the pipeline: `python -m $package`

## Data

See [docs/DATA.md](docs/DATA.md).

## Citation

See [CITATION.cff](CITATION.cff).

## License

Code: $license. Data: see docs/DATA.md.
"""

GITIGNORE = """# Data (keep out of git; document sources in docs/DATA.md)
data/raw/*
data/interim/*
data/processed/*
!data/**/.gitkeep
# Generated results
results/**/*.png
results/**/*.pdf
results/runs/
models/
# Python
__pycache__/
*.py[cod]
.venv/
.ipynb_checkpoints/
# OS / editors
.DS_Store
Thumbs.db
.vscode/
.idea/
# Secrets
.env
*.key
"""

DATA_MD = """# Data

| Dataset | Source / DOI | Licence | Retrieved | Location | SHA-256 |
|---------|--------------|---------|-----------|----------|---------|
|         |              |         |           | data/raw/ |        |

## Processing

Describe each step from `data/raw` to `data/processed` and the script that performs it.

## Personal data

State whether the data contain personal information, the legal basis, and how they are protected.
"""

CITATION = """cff-version: 1.2.0
message: "If you use this work, please cite it as below."
title: "$title"
authors:
  - family-names: "$family"
    given-names: "$given"$orcid_cff
date-released: "$date"
license: $license_id
"""

INIT_PY = '"""$title."""\n\n__version__ = "0.1.0"\n'
MAIN_PY = '''"""Run the analysis pipeline: python -m $package"""


def main():
    print("Implement the pipeline steps here (load -> clean -> analyse -> report).")


if __name__ == "__main__":
    main()
'''
LICENSES = {"MIT": "MIT", "Apache-2.0": "Apache-2.0", "GPL-3.0": "GPL-3.0-or-later", "BSD-3-Clause": "BSD-3-Clause",
            "CC-BY-4.0": "CC-BY-4.0"}

TEMPLATES = {"basic": "data, code, results, docs", "ml": "basic + models/, configs/, results/runs/",
             "paper": "basic + manuscript/ for LaTeX/Markdown writing"}


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
    return ("p_" + s if s[:1].isdigit() else s) or "project"


def plan(title, author, template="basic", description="", license="MIT", orcid="", package=None, date=None):
    """Return (dirs, files) to create, with paths relative to the project root."""
    if template not in TEMPLATES:
        raise ValueError("unknown template %r" % template)
    if license not in LICENSES:
        raise ValueError("license must be one of %s" % ", ".join(LICENSES))
    pkg = package or slugify(title)
    given, _, family = author.rpartition(" ")
    extra = EXTRA_DIRS[template]
    v = {"title": title, "description": description or "One-paragraph summary of the research question.",
         "author": author, "orcid_line": " (ORCID %s)" % orcid if orcid else "", "date": date or datetime.date.today().isoformat(),
         "package": pkg, "license": license, "license_id": LICENSES[license],
         "family": family or author, "given": given, "orcid_cff": '\n    orcid: "https://orcid.org/%s"' % orcid if orcid else "",
         "extra_tree": "".join("%-19s\n" % (d + "/") for d in extra)}
    dirs = [string.Template(d).substitute(v) for d in BASE_DIRS + extra]
    files = {
        "README.md": string.Template(README).substitute(v),
        ".gitignore": GITIGNORE,
        "docs/DATA.md": DATA_MD,
        "CITATION.cff": string.Template(CITATION).substitute(v),
        "requirements.txt": "# pin versions, e.g. numpy==2.1.0\n",
        "src/%s/__init__.py" % pkg: string.Template(INIT_PY).substitute(v),
        "src/%s/__main__.py" % pkg: string.Template(MAIN_PY).substitute(v),
        "tests/test_smoke.py": "def test_import():\n    import %s  # noqa: F401\n" % pkg,
    }
    for d in ("data/raw", "data/interim", "data/processed", "results/figures", "results/tables"):
        files[d + "/.gitkeep"] = ""
    if template == "paper":
        files["manuscript/main.md"] = "# %s\n\n## Abstract\n\n## Introduction\n\n## Methods\n\n## Results\n\n## Discussion\n" % title
    if template == "ml":
        files["configs/default.json"] = '{\n  "seed": 42,\n  "learning_rate": 0.001,\n  "batch_size": 32\n}\n'
    return dirs, files


def create(root, dirs, files, overwrite=False):
    """Create the layout. Returns (created, skipped) lists of relative paths."""
    created, skipped = [], []
    for d in dirs:
        os.makedirs(os.path.join(root, d), exist_ok=True)
    for rel, text in files.items():
        path = os.path.join(root, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.exists(path) and not overwrite:
            skipped.append(rel)
            continue
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        created.append(rel)
    return created, skipped
