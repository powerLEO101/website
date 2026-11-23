#!/usr/bin/env python3
"""Run python3 generate.py in your content directory. Requires pandoc."""

from pathlib import Path
import shutil
import subprocess


def main():
    if not shutil.which("pandoc"):
        raise SystemExit("Install pandoc first, then run python3 generate.py.")

    extensions = {".md", ".markdown", ".rst", ".org", ".txt", ".textile",
                  ".html", ".htm", ".docx", ".odt", ".tex"}
    sources = sorted(p for p in Path.cwd().iterdir()
                     if p.is_file() and not p.name.startswith(".")
                     and p.suffix.lower() in extensions)
    if not sources:
        raise SystemExit("No supported documents found in the current directory.")
    if len({p.stem for p in sources}) != len(sources):
        raise SystemExit("Documents with the same stem would overwrite each other; rename them first.")

    assets = Path(__file__).resolve().parent
    output = Path("site")
    output.mkdir(exist_ok=True)
    for source in sources:
        command = ["pandoc", str(source), "--standalone", "--to=html5",
                   "--template", str(assets / "page.template"),
                   "--css", str(assets / "style.css"),
                   "--metadata", "pagetitle=" + source.stem,
                   "--embed-resources", "--output", str(output / (source.stem + ".html"))]
        if source.suffix.lower() == ".txt":
            command.extend(["--from", "markdown"])
        subprocess.run(command, check=True)
        print(output / (source.stem + ".html"))


if __name__ == "__main__":
    main()
