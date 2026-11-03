# kegedy.github.io

Personal projects site: circuit write-ups (Markdown + LaTeX), schematics, and
interactive GDS layouts.

| Part | Where it lives | Deployed to |
|---|---|---|
| Website ([Docusaurus](https://docusaurus.io)) | `docs/`, `src/`, `static/` | GitHub Pages: https://kegedy.github.io |
| Layout viewer ([kweb](https://github.com/gdsfactory/kweb)) | `kweb/`, `gds/` | Hugging Face Space: https://kegedy-gds-viewer.hf.space |

Both deploy automatically on push to `main` (`.github/workflows/`).

## Add a project

1. Copy `templates/project-template.mdx` to `docs/<project>/index.mdx`.
2. Export the schematic (see below) and put plots in `docs/<project>/`.
3. Put the layout in `gds/<project>.gds` and reference it with
   `<LayoutViewer file="<project>.gds" cell="TOP" />`.
4. Add a row to the table in `docs/index.mdx`, then push.

Layer names and colors come from `gds/sky130A.lyp` (copied from the sky130A PDK's
`libs.tech/klayout/tech/`), which `LayoutViewer` uses by default. For another PDK, drop its
`.lyp` into `gds/` and pass `layerProps="other.lyp"`; `layerProps={null}` shows raw numbers.

Link between pages by file path, e.g. `[text](./other-project/index.mdx)`.

## Run locally

Node comes from the `web` conda env: `conda activate web`.

```bash
npm install                      # first time only
npm start                        # site at http://localhost:3000
```

To see layouts locally, start kweb in a second terminal and point the site at it:

```bash
cd kweb && python -m venv .venv && .venv/bin/pip install -r requirements.txt   # first time only
GDS_DIR=../gds .venv/bin/uvicorn app:app --port 8765

KWEB_URL=http://localhost:8765 npm start
```

## 3D views (gdsfactory)

```bash
python -m venv scripts/.venv && scripts/.venv/bin/pip install gdsfactory trimesh   # first time only
scripts/.venv/bin/python scripts/gds3d.py gds/<project>.gds [--cell TOP]
```

This writes `static/models/<project>.glb` and its legend `<project>.json` (commit both). Add
`model="<project>.glb"` to the page's `<LayoutViewer>` for a 2D/3D toggle, or show the 3D view on
its own with `<LayoutViewer3D model="<project>.glb" />`. Layer heights/thicknesses for sky130 are in
`SKY130_STACK` in `scripts/gds3d.py`; colors come from `gds/sky130A.lyp`.

## Schematics from xschem

Keep the schematic source in `xschem/<project>.sch` and export it with:

```bash
scripts/schematic_svg.sh xschem/<project>.sch
```

This writes `static/schematics/<project>.svg` (commit it) in xschem's own colors, with the sky130
simulation annotations (`id=`, `gm=`, …) hidden. Show it zoomable with
`<SchematicViewer file="<project>.svg" />`. Needs a display (WSLg is fine) for correct text placement.
