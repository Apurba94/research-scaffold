"""Command-line interface for research-scaffold."""
import argparse
import os
import subprocess

from .core import LICENSES, TEMPLATES, create, plan, slugify


def main(argv=None):
    ap = argparse.ArgumentParser(prog="research-scaffold", description="Create a reproducible research project layout.")
    ap.add_argument("title", help="project title")
    ap.add_argument("-a", "--author", required=True)
    ap.add_argument("-d", "--directory", help="target directory (default: slug of the title)")
    ap.add_argument("-t", "--template", choices=sorted(TEMPLATES), default="basic")
    ap.add_argument("--description", default="")
    ap.add_argument("--license", choices=sorted(LICENSES), default="MIT")
    ap.add_argument("--orcid", default="")
    ap.add_argument("--git", action="store_true", help="run git init in the new project")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    root = args.directory or slugify(args.title).replace("_", "-")
    dirs, files = plan(args.title, args.author, args.template, args.description, args.license, args.orcid)
    if args.dry_run:
        for d in dirs:
            print("dir  " + d)
        for f in files:
            print("file " + f)
        return 0
    created, skipped = create(root, dirs, files)
    print("%s: %d file(s) created, %d existing file(s) kept" % (root, len(created), len(skipped)))
    if args.git and not os.path.isdir(os.path.join(root, ".git")):
        subprocess.run(["git", "init", "-q"], cwd=root)
        print("initialized git repository")
    return 0
