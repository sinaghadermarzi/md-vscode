# md-vscode

A VS Code workspace for writing Markdown and turning it into PDFs with Pandoc + Tectonic. Works
locally (if you have Pandoc and Tectonic installed) or inside the included Dev Container.

The `.gitignore` ignores everything except the configuration below, so you can drop your own `.md`
files (and the generated `.tex`/`.pdf`) into this folder without committing them.

## What is in the repo

| Path | Purpose |
| --- | --- |
| `.vscode/tasks.json` | The two VS Code tasks described below. |
| `.vscode/settings.json` | Turns off LaTeX Workshop auto-build (the extension is only used to view PDFs). |
| `.pandoc-templates/minimal-numbered.latex` | Pandoc LaTeX template used by the build task: Open Sans (scaled 0.85), A4, 1in margins, 1.25 line spacing, numbered headings, colored links, `longtable` tables, figures kept in place. Requires Pandoc 3.x (`\pandocbounded`). |
| `.pandoc-templates/minimal.latex` | Same template with unnumbered headings. Not referenced by the tasks; swap it into the build command if you prefer it. |
| `.pandoc-templates/md2tex.py` | Small stdlib-only Markdown -> LaTeX converter (headings, nested lists, tables, images, bold/italic/code, with math left untouched). Reads a file or stdin, prints LaTeX. |
| `.vscode/format-deep-research.py` | Cleans ChatGPT Deep Research Markdown before conversion: entity markers become `**name** (description)`, citation markers are removed (or `--citations footnote|bracket`), `image_group{...}` blocks are dropped, whitespace is tidied. |
| `.devcontainer/` | Ubuntu Dev Container with Pandoc, Open Sans, `librsvg2-bin` (SVG images) and Tectonic (installed via Homebrew), plus Markdown extensions and LaTeX Workshop. |

## Usage

### In VS Code

1. Open the folder (locally, or with **Dev Containers: Reopen in Container**).
2. Open a Markdown file and run **Terminal > Run Build Task** (`Ctrl/Cmd+Shift+B`), which is the
   **Compile Markdown to PDF** task. It writes `<name>.tex` (from `md2tex.py`) and `<name>.pdf` next
   to the Markdown file. The PDF is produced by Pandoc directly from the Markdown with the
   `minimal-numbered.latex` template; the `.tex` file is a plain-LaTeX side product you can edit by hand.
3. For a Deep Research export, run the **Format Deep Research Markdown** task first (`Terminal > Run
   Task...`). It rewrites the open file in place.

### From the command line

```sh
# Optional: clean a ChatGPT Deep Research export (writes <name>-formatted.md, or --inplace)
python3 .vscode/format-deep-research.py notes.md

# Markdown -> LaTeX
python3 .pandoc-templates/md2tex.py notes.md > notes.tex

# Markdown -> PDF (what the build task runs)
pandoc notes.md -o notes.pdf --pdf-engine=tectonic --resource-path=. \
  --template=.pandoc-templates/minimal-numbered.latex --highlight-style=tango \
  --from markdown+tex_math_single_backslash+tex_math_dollars
```

Requirements outside the container: Python 3, Pandoc 3.x, [Tectonic](https://tectonic-typesetting.github.io/)
and the Open Sans font (`fonts-open-sans` on Debian/Ubuntu). Tectonic fetches the LaTeX packages it needs on
first run, so the first build needs network access.
