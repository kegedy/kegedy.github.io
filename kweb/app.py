"""kweb server for the layout viewer. Serves every GDS/OAS file in ./gds (read-only)."""

import json
import os
from pathlib import Path

import klayout.db as db
from kweb.api import viewer as kweb_viewer
from kweb.browser import get_app
from kweb.layout_server import LayoutViewServerEndpoint

# Workaround for kweb 2.0.4: with a .lyp that lists layers the layout doesn't use
# (e.g. the full sky130A.lyp), kweb calls bbox_per_layer with an invalid index
# (-1 as unsigned) and the websocket crashes. Treat those layers as empty.
_bbox_per_layer = db.Cell.bbox_per_layer


def _safe_bbox_per_layer(cell: db.Cell, layer_index: int) -> db.Box:
    if not 0 <= layer_index <= 0xFFFFFFFF:
        return db.Box()
    return _bbox_per_layer(cell, layer_index)


db.Cell.bbox_per_layer = _safe_bbox_per_layer

# Tell the page which layers the shapes selected on the canvas are on, so the layer list
# can highlight them. kweb has no such message; sent as {"msg": "selection-layers", "ids": [...]}
# (layer list ids) after any message that can change the selection, only when it changed.
_SELECTION_MSGS = {"mouse_released", "mouse_dblclick", "keydown", "ci-s", "cell-s", "reload"}
_reader = LayoutViewServerEndpoint.reader


def _selected_layer_ids(view) -> list[int]:
    selected = {
        (path.cv_index, path.layer)
        for path in view.each_object_selected()
        if not path.is_cell_inst()
    }
    ids = []
    it = view.begin_layers()
    while not it.at_end():
        node = it.current()
        if not node.has_children() and (node.cellview(), node.layer_index()) in selected:
            ids.append(node.id())
        it.next()
    return ids


async def _reader_with_selection(self, websocket, data: str) -> None:
    await _reader(self, websocket, data)
    if json.loads(data).get("msg") not in _SELECTION_MSGS:
        return
    ids = _selected_layer_ids(self.layout_view)
    if ids != getattr(self, "_last_selection_ids", []):
        self._last_selection_ids = ids
        await websocket.send_text(json.dumps({"msg": "selection-layers", "ids": ids}))


LayoutViewServerEndpoint.reader = _reader_with_selection

# Templates in ./templates override kweb's own (viewer.html: collapsible layer panel on the left)
kweb_viewer.templates.env.loader.searchpath.insert(
    0, str(Path(__file__).resolve().parent / "templates")
)

gds_dir = Path(os.environ.get("GDS_DIR", Path(__file__).resolve().parent / "gds"))

app = get_app(fileslocation=gds_dir, editable=False)
