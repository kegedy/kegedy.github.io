"""Convert a sky130 GDS into a 3D model (.glb + legend .json) with gdsfactory, for <LayoutViewer3D>.

Usage: scripts/.venv/bin/python scripts/gds3d.py gds/<name>.gds [--cell CELL] [--out static/models/<name>.glb]

Each layer is extruded between its sky130 zmin and zmin + thickness (microns, silicon
surface at z = 0). Thicknesses follow the sky130 process description shipped with the PDK
(libs.tech/klayout/tech/xsect/sky130.xs). Colors come from gds/sky130A.lyp, the same file
the 2D viewer uses. Wells and implants are left out so the devices stay visible.
"""

import argparse
import json
from pathlib import Path

import gdsfactory as gf
from gdsfactory.technology import LayerLevel, LayerStack, LayerViews, LogicalLayer

REPO = Path(__file__).resolve().parent.parent

# name: (layer, zmin, thickness) in microns
SKY130_STACK = {
    "diff": ((65, 20), -0.12, 0.12),
    "tap": ((65, 44), -0.12, 0.12),
    "poly": ((66, 20), 0.0, 0.18),
    "licon1": ((66, 44), 0.0, 0.94),
    "li1": ((67, 20), 0.94, 0.10),
    "mcon": ((67, 44), 1.04, 0.43),
    "met1": ((68, 20), 1.47, 0.36),
    "via": ((68, 44), 1.83, 0.27),
    "met2": ((69, 20), 2.10, 0.36),
    "via2": ((69, 44), 2.46, 0.42),
    "met3": ((70, 20), 2.88, 0.845),
    "via3": ((70, 44), 3.725, 0.39),
    "met4": ((71, 20), 4.115, 0.845),
    "via4": ((71, 44), 4.96, 0.505),
    "met5": ((72, 20), 5.465, 1.26),
}


# In sky130A.lyp, contacts/vias are near-white like li1, which washes out in 3D
CONTACT_COLOR = "#808080"
CONTACTS = ["licon1", "mcon", "via", "via2", "via3", "via4"]


def layer_views() -> LayerViews:
    views = LayerViews.from_lyp(REPO / "gds" / "sky130A.lyp")
    for name in CONTACTS:
        view = views.get_from_tuple(SKY130_STACK[name][0])
        color = type(view.fill_color)(CONTACT_COLOR)
        view.fill_color = color
        view.frame_color = color
    return views


def layer_stack() -> LayerStack:
    return LayerStack(
        layers={
            name: LayerLevel(layer=LogicalLayer(layer=layer), zmin=zmin, thickness=thickness)
            for name, (layer, zmin, thickness) in SKY130_STACK.items()
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("gds", type=Path)
    parser.add_argument("--cell", help="cell to export (default: top cell)")
    parser.add_argument("--out", type=Path, help="default: static/models/<gds name>.glb")
    args = parser.parse_args()

    out = args.out or REPO / "static" / "models" / f"{args.gds.stem}.glb"
    out.parent.mkdir(parents=True, exist_ok=True)

    gf.gpdk.PDK.activate()
    component = gf.import_gds(args.gds, cellname=args.cell)
    views = layer_views()
    scene = component.to_3d(layer_views=views, layer_stack=layer_stack())
    scene.export(out)
    print(f"wrote {out} ({out.stat().st_size / 1024:.0f} KB, {len(scene.geometry)} meshes)")

    # Legend for <LayoutViewer3D>: layers present in the model, top of the stack first
    present = component.get_polygons_points(merge=True)
    legend = [
        {
            "name": name,
            "color": views.get_from_tuple(layer).fill_color.as_hex(format="long"),
            "zmin": zmin,
            "zmax": round(zmin + thickness, 3),
        }
        for name, (layer, zmin, thickness) in reversed(SKY130_STACK.items())
        if int(gf.get_layer(layer)) in present
    ]
    legend_path = out.with_suffix(".json")
    legend_path.write_text(json.dumps(legend, indent=2) + "\n")
    print(f"wrote {legend_path} ({len(legend)} layers)")


if __name__ == "__main__":
    main()
