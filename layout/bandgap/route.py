"""A small grid router for the bandgap: connects every net on met2, met3 and met4.

How it works:

- The routing grid has a 1.0 um pitch on met2, met3 and met4, with 0.4 um wires. That
  leaves 0.6 um between neighbouring tracks, which clears every spacing rule on those
  layers with margin, so the router only has to keep each grid node to one net.
- Each device terminal gets one access point:
  - metal-1 terminals: a met1 pad and via1 placed where the pad clears other met1;
  - li-only terminals (bulk taps, PNP base/collector rings): an mcon and pad on the li,
    or, if there is no room, a short li stub out to free space;
  - MIM cap plates, which come up to met4: met4 grid nodes inside the plate's met4.
  A short met2 stub joins an off-grid via to the nearest free grid node. Grid nodes near a
  stub are reserved for its net, so stubs keep their spacing too.
- Existing device metal on met2-met4 (the MIM cap) blocks nodes for other nets.
- Nets are routed one at a time with A* (met2 prefers vertical, met3 horizontal), each
  pin joining the net's tree. If a net fails, all routes are ripped up and the failed net
  goes first next time.
"""

import heapq
import itertools

import klayout.db as kdb

LAYER = {
    "li": (67, 20), "mcon": (67, 44), "met1": (68, 20), "via1": (68, 44), "met2": (69, 20),
    "via2": (69, 44), "met3": (70, 20), "via3": (70, 44), "met4": (71, 20),
}
LABEL = {"met2": (69, 5), "met3": (70, 5), "met4": (71, 5)}
ZL = ["met2", "met3", "met4"]
SPACE = {"met1": 0.14, "met2": 0.14, "met3": 0.36, "met4": 0.36, "li": 0.17}  # met3/4 include the 0.05 of a 0.5 node pad
PITCH, W = 1.0, 0.4
NODE = {"met2": W, "met3": 0.5, "met4": 0.5}  # node squares: 0.5 on met3/met4 clears the 0.24 um2 min area
PAD = 0.32      # met1 / met2 landing pad around via1 (and mcon)
MARGIN = 3.0    # um of routing space around the placed devices


def d(x):
    """um -> dbu, snapped to the 5 nm manufacturing grid."""
    return int(round(x / 0.005)) * 5


def box(cx, cy, w, h=None):
    h = w if h is None else h
    return kdb.Box(d(cx - w / 2), d(cy - h / 2), d(cx + w / 2), d(cy + h / 2))


class Router:
    def __init__(self, layout, top):
        self.layout, self.top = layout, top
        b = top.dbbox()
        self.x0, self.y0 = b.left - MARGIN, b.bottom - MARGIN
        self.ni = int((b.width() + 2 * MARGIN) / PITCH) + 1
        self.nj = int((b.height() + 2 * MARGIN) / PITCH) + 1
        self.all = {k: kdb.Region(top.begin_shapes_rec(layout.layer(*LAYER[k]))) for k in
                    ("li", "met1", "met2", "met3", "met4")}
        for r in self.all.values():
            r.merge()
        self.added = {k: kdb.Region() for k in ("li", "met1")}   # pads and stubs added so far
        self.met2_by_net = {}      # net -> Region of met2 added for pin access
        self.blocked = set()       # nodes nobody may use
        self.owner = {}            # node -> the only net allowed to use it
        self.eblocked = set()      # same for wire segments between neighbouring nodes
        self.eowner = {}
        self.no_via3 = set()       # (i, j) where a via3 would sit too close to an existing one
        self.pins = {}             # net -> list of pin node sets
        self.extra = []            # (layer, box) shapes added for pin access
        self.routes = {}           # net -> list of node paths

    # ---- grid ----------------------------------------------------------------
    def xy(self, i, j):
        return self.x0 + i * PITCH, self.y0 + j * PITCH

    def nodes_near(self, z, dbox, clearance):
        """Nodes on layer z whose wire square comes within `clearance` um of dbox (dbu box)."""
        r = W / 2 + clearance
        x1, y1 = dbox.left * 0.001 - r, dbox.bottom * 0.001 - r
        x2, y2 = dbox.right * 0.001 + r, dbox.top * 0.001 + r
        i1, i2 = max(0, int((x1 - self.x0) / PITCH) - 1), min(self.ni - 1, int((x2 - self.x0) / PITCH) + 1)
        j1, j2 = max(0, int((y1 - self.y0) / PITCH) - 1), min(self.nj - 1, int((y2 - self.y0) / PITCH) + 1)
        for i in range(i1, i2 + 1):
            for j in range(j1, j2 + 1):
                x, y = self.xy(i, j)
                if x1 < x < x2 and y1 < y < y2:
                    yield (z, i, j)

    def claim(self, node, net):
        if node in self.blocked:
            return
        o = self.owner.get(node)
        if o is None:
            self.owner[node] = net
        elif o != net:
            self.blocked.add(node)

    def free_for(self, node, net):
        return node not in self.blocked and self.owner.get(node, net) == net

    @staticmethod
    def edge(a, b):
        return (a, b) if a < b else (b, a)

    def claim_edge(self, e, net):
        if e in self.eblocked:
            return
        o = self.eowner.get(e)
        if net is None or (o is not None and o != net):
            self.eblocked.add(e)
        elif o is None:
            self.eowner[e] = net

    def edge_free(self, e, net):
        return e not in self.eblocked and self.eowner.get(e, net) == net

    def keep_out(self, z, region, clearance, net):
        """Reserve for `net` (None: block for everyone) every node and wire segment on layer z
        whose metal would come within `clearance` um of `region`."""
        grown = region.sized(d(clearance))
        for poly in region.each():
            for node in self.nodes_near(z, poly.bbox(), clearance + PITCH):
                x, y = self.xy(*node[1:])
                if not (kdb.Region(box(x, y, W)) & grown).is_empty():
                    if net is None:
                        self.blocked.add(node)
                    else:
                        self.claim(node, net)
                for di, dj in ((1, 0), (0, 1)):
                    m = (z, node[1] + di, node[2] + dj)
                    if m[1] >= self.ni or m[2] >= self.nj:
                        continue
                    seg = kdb.Box(d(x - W / 2), d(y - W / 2), d(x + di * PITCH + W / 2), d(y + dj * PITCH + W / 2))
                    if not (kdb.Region(seg) & grown).is_empty():
                        self.claim_edge(self.edge(node, m), net)

    # ---- static obstacles ----------------------------------------------------
    def add_obstacles(self, net_shapes):
        """net_shapes: {layer: {net: Region}} for device metal on met2-met4."""
        for z, lay in enumerate(ZL):
            known = kdb.Region()
            for net, reg in net_shapes.get(lay, {}).items():
                known += reg
                self.keep_out(z, reg, SPACE[lay], net)
            self.keep_out(z, self.all[lay] - known, SPACE[lay], None)
        # capm.2b: other met3 must stay 1.2 um from a MIM cap's bottom plate (under capm)
        capm = kdb.Region(self.top.begin_shapes_rec(self.layout.layer(89, 44)))
        plate = self.all["met3"] & capm.sized(d(0.5))
        if not plate.is_empty():
            self.keep_out(1, self.all["met3"].interacting(plate), 1.2 + 0.05, None)
        # via3.2: keep new via3 0.2 um (+ margin) from the cap's own via3 array
        via3 = kdb.Region(self.top.begin_shapes_rec(self.layout.layer(*LAYER["via3"])))
        grown = via3.sized(d(0.2 + 0.05))
        for poly in via3.each():
            for node in self.nodes_near(1, poly.bbox(), 0.5):
                if not (kdb.Region(box(*self.xy(*node[1:]), 0.2)) & grown).is_empty():
                    self.no_via3.add(node[1:])

    # ---- pin access ----------------------------------------------------------
    def _commit(self, net, node, shapes):
        """Add access shapes and reserve grid nodes near any new met2 for this net."""
        for lay, b in shapes:
            self.extra.append((lay, b))
            if lay in self.added:
                self.added[lay].insert(b)
            if lay == "met2":
                self.keep_out(0, kdb.Region(b), SPACE["met2"] + 0.02, net)
                self.met2_by_net.setdefault(net, kdb.Region()).insert(b)
        self.claim(node, net)
        self.met2_by_net.setdefault(net, kdb.Region()).insert(box(*self.xy(*node[1:]), W))
        self.pins.setdefault(net, []).append({node})

    def _via_options(self, net, centres):
        """For candidate via1 centres, the free grid node with the shortest met2 stub."""
        best = None
        for (vx, vy) in centres:
            i, j = round((vx - self.x0) / PITCH), round((vy - self.y0) / PITCH)
            for di, dj in itertools.product((0, -1, 1), repeat=2):
                node = (0, i + di, j + dj)
                if not (0 <= node[1] < self.ni and 0 <= node[2] < self.nj) or not self.free_for(node, net):
                    continue
                gx, gy = self.xy(*node[1:])
                cost = abs(gx - vx) + abs(gy - vy)
                if best is not None and cost >= best[0]:
                    continue
                # the pad, stub and node square must clear other nets' access met2
                mine = kdb.Region()
                for _, b in self._stub((vx, vy), node):
                    mine.insert(b)
                mine.insert(box(gx, gy, W))
                foreign = kdb.Region()
                for other, reg in self.met2_by_net.items():
                    if other != net:
                        foreign += reg
                if not (mine & foreign.sized(d(SPACE["met2"] + 0.02))).is_empty():
                    continue
                best = (cost, (vx, vy), node)
        return best

    def _stub(self, v, node):
        """met2 from the via at v to grid node: an L of rectangles exactly W wide (as wide as
        the node squares), so the pieces line up with no small steps or notches."""
        gx, gy = self.xy(*node[1:])
        vx, vy = v
        h = W / 2
        if min(abs(gx - vx), abs(gy - vy)) < 0.3:
            # nearly aligned: one rectangle, since an L would leave a step under m2 spacing
            return [("met2", kdb.Box(d(min(vx, gx) - h), d(min(vy, gy) - h), d(max(vx, gx) + h), d(max(vy, gy) + h)))]
        return [("met2", kdb.Box(d(min(vx, gx) - h), d(vy - h), d(max(vx, gx) + h), d(vy + h))),
                ("met2", kdb.Box(d(gx - h), d(min(vy, gy) - h), d(gx + h), d(max(vy, gy) + h)))]

    @staticmethod
    def _centres(region, step=0.05):
        """Sample points inside a region (um)."""
        pts = []
        for poly in region.each():
            bb = poly.bbox()
            x = bb.left * 0.001
            while x <= bb.right * 0.001 + 1e-9:
                y = bb.bottom * 0.001
                while y <= bb.top * 0.001 + 1e-9:
                    if poly.inside(kdb.Point(d(x), d(y))):
                        pts.append((round(x / 0.005) * 0.005, round(y / 0.005) * 0.005))
                    y += step
                x += step
        return pts

    def access(self, net, term_shapes):
        """term_shapes: {layer: Region} of one terminal, in top-cell coordinates."""
        if "met4" in term_shapes:              # MIM plate: land on its met4 directly
            reg = term_shapes["met4"]
            other4 = (self.all["met4"] - reg).sized(d(SPACE["met4"] + 0.05))
            nodes, bridges = set(), []
            for poly in reg.each():
                bb = poly.bbox()
                for node in self.nodes_near(2, bb, PITCH):
                    if not self.free_for(node, net):
                        continue
                    x, y = self.xy(*node[1:])
                    sq = box(x, y, W)
                    if (kdb.Region(sq) - reg).is_empty():          # wire square fully on the plate
                        nodes.add(node)
                    elif bb.width() < d(1.0) and bb.bottom + d(W) < d(y) < bb.top - d(W):
                        # narrow strip (the bottom plate's met4): bridge across to its centre
                        cx = bb.center().x * 0.001
                        br = kdb.Box(d(min(x, cx) - W / 2), d(y - W / 2), d(max(x, cx) + W / 2), d(y + W / 2))
                        if (kdb.Region(br) & other4).is_empty():
                            nodes.add(node)
                            bridges.append(br)
            if not nodes:
                raise RuntimeError(f"{net}: no met4 access on the MIM plate")
            for br in bridges:
                self.extra.append(("met4", br))
            for n in nodes:
                self.claim(n, net)
            self.pins.setdefault(net, []).append(nodes)
            return
        keep_out = (self.all["met1"] + self.added["met1"]) - term_shapes.get("met1", kdb.Region())
        keep_out = keep_out.sized(d(PAD / 2 + SPACE["met1"] + 0.01))
        if "met1" in term_shapes:
            ok = term_shapes["met1"] - keep_out
            best = self._via_options(net, self._centres(ok))
            if best:
                _, v, node = best
                self._commit(net, node, [("met1", box(*v, PAD)), ("via1", box(*v, 0.15))] + self._stub(v, node))
                return
        li = term_shapes.get("li", kdb.Region())
        ok = li.sized(-d(0.085)) - keep_out          # where a 0.17 mcon fits inside the li
        best = self._via_options(net, self._centres(ok))
        if best:
            _, v, node = best
            self._commit(net, node, [("mcon", box(*v, 0.17)), ("met1", box(*v, PAD)), ("via1", box(*v, 0.15))]
                         + self._stub(v, node))
            return
        self._li_stub(net, li, keep_out)

    def _li_stub(self, net, li, keep_out):
        """No room on the li itself: run a 0.29 um li stub out to free space, then mcon + via."""
        other_li = (self.all["li"] + self.added["li"]) - li
        guard = other_li.sized(d(SPACE["li"] + 0.01))
        for poly in li.each():
            bb = poly.bbox()
            cx, cy = bb.center().x * 0.001, bb.center().y * 0.001
            for frac in (0.5, 0.3, 0.7, 0.15, 0.85):
                starts = [("+x", bb.right * 0.001, bb.bottom * 0.001 + frac * bb.height() * 0.001),
                          ("-x", bb.left * 0.001, bb.bottom * 0.001 + frac * bb.height() * 0.001),
                          ("+y", bb.left * 0.001 + frac * bb.width() * 0.001, bb.top * 0.001),
                          ("-y", bb.left * 0.001 + frac * bb.width() * 0.001, bb.bottom * 0.001)]
                for direction, sx, sy in starts:
                    for length in [0.6 + 0.2 * k for k in range(13)]:
                        dx, dy = {"+x": (1, 0), "-x": (-1, 0), "+y": (0, 1), "-y": (0, -1)}[direction]
                        ex, ey = sx + dx * length, sy + dy * length
                        stub = kdb.Box(d(min(sx, ex) - (0.145 if dy else 0)), d(min(sy, ey) - (0.145 if dx else 0)),
                                       d(max(sx, ex) + (0.145 if dy else 0)), d(max(sy, ey) + (0.145 if dx else 0)))
                        # end the stub with a 0.29 square so the mcon sits fully inside li
                        end = box(ex - dx * 0.145, ey - dy * 0.145, 0.29)
                        stub_r = kdb.Region(stub) + kdb.Region(end)
                        v = (ex - dx * 0.145, ey - dy * 0.145)
                        if not (stub_r & guard).is_empty():
                            continue
                        if not (kdb.Region(box(*v, 0.01)) & keep_out).is_empty():
                            continue
                        best = self._via_options(net, [v])
                        if best:
                            _, v, node = best
                            self._commit(net, node, [("li", stub), ("li", end), ("mcon", box(*v, 0.17)),
                                                     ("met1", box(*v, PAD)), ("via1", box(*v, 0.15))]
                                         + self._stub(v, node))
                            return
        raise RuntimeError(f"{net}: no access point found for an li terminal")

    # ---- routing -------------------------------------------------------------
    def _neighbours(self, node):
        z, i, j = node
        pref = {0: (0, 1), 1: (1, 0), 2: None}[z]   # met2 vertical, met3 horizontal
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ii, jj = i + di, j + dj
            if 0 <= ii < self.ni and 0 <= jj < self.nj:
                cost = 1.0 if pref is None or (abs(di), abs(dj)) == pref else 2.0
                yield (z, ii, jj), cost
        for dz in (-1, 1):
            if 0 <= z + dz < 3:
                yield (z + dz, i, j), 3.0

    def _astar(self, net, sources, targets):
        ti = [n[1] for n in targets]
        tj = [n[2] for n in targets]
        bi, bj = (min(ti), max(ti)), (min(tj), max(tj))

        def h(n):
            return max(0, bi[0] - n[1], n[1] - bi[1]) + max(0, bj[0] - n[2], n[2] - bj[1])

        counter = itertools.count()
        openq = [(h(s), next(counter), 0.0, s) for s in sources]
        heapq.heapify(openq)
        came, g = {s: None for s in sources}, {s: 0.0 for s in sources}
        while openq:
            _, _, cost, n = heapq.heappop(openq)
            if n in targets:
                path = [n]
                while came[path[-1]] is not None:
                    path.append(came[path[-1]])
                return path
            if cost > g.get(n, 1e18):
                continue
            for m, step in self._neighbours(n):
                if not self.free_for(m, net):
                    continue
                if m[0] == n[0] and not self.edge_free(self.edge(n, m), net):
                    continue
                if {m[0], n[0]} == {1, 2} and n[1:] in self.no_via3:
                    continue
                c = cost + step
                if c < g.get(m, 1e18):
                    g[m], came[m] = c, n
                    heapq.heappush(openq, (c + h(m), next(counter), c, m))
        return None

    def route_net(self, net):
        pins = self.pins[net]
        tree = set(pins[0])
        paths = []
        remaining = list(pins[1:])
        while remaining:
            ci = sum(n[1] for n in tree) / len(tree)
            cj = sum(n[2] for n in tree) / len(tree)
            remaining.sort(key=lambda p: min(abs(n[1] - ci) + abs(n[2] - cj) for n in p))
            pin = remaining.pop(0)
            if pin & tree:
                continue
            path = self._astar(net, pin, tree)
            if path is None:
                return None
            for n in path:
                self.claim(n, net)
            for a, b in zip(path, path[1:]):
                if a[0] == b[0]:
                    self.claim_edge(self.edge(a, b), net)
            tree |= set(path)
            paths.append(path)
        return paths

    def route_all(self, order, tries=8):
        base = (dict(self.owner), set(self.blocked), dict(self.eowner), set(self.eblocked))
        for attempt in range(tries):
            self.owner, self.blocked = dict(base[0]), set(base[1])
            self.eowner, self.eblocked, self.routes = dict(base[2]), set(base[3]), {}
            failed = []
            for net in order:
                paths = self.route_net(net)
                if paths is None:
                    failed.append(net)
                else:
                    self.routes[net] = paths
            if not failed:
                return attempt + 1
            order = failed + [n for n in order if n not in failed]
        raise RuntimeError(f"routing failed for {failed} after {tries} attempts")

    # ---- output --------------------------------------------------------------
    def write_shapes(self, labels):
        sh = lambda lay: self.top.shapes(self.layout.layer(*LAYER[lay]))  # noqa: E731
        for lay, b in self.extra:
            sh(lay).insert(b)
        for net, pins in self.pins.items():
            for pin in pins:
                for n in pin:
                    if n[0] == 0:                  # met2 square under each via1 grid node
                        sh("met2").insert(box(*self.xy(*n[1:]), W))
        for net, paths in self.routes.items():
            for path in paths:
                for a, b in zip(path, path[1:]):
                    (za, ia, ja), (zb, ib, jb) = a, b
                    xa, ya = self.xy(ia, ja)
                    xb, yb = self.xy(ib, jb)
                    if za == zb:
                        sh(ZL[za]).insert(kdb.Box(d(min(xa, xb) - W / 2), d(min(ya, yb) - W / 2),
                                                   d(max(xa, xb) + W / 2), d(max(ya, yb) + W / 2)))
                    else:
                        lo = min(za, zb)
                        sh(ZL[lo]).insert(box(xa, ya, NODE[ZL[lo]]))
                        sh(ZL[lo + 1]).insert(box(xa, ya, NODE[ZL[lo + 1]]))
                        sh(["via2", "via3"][lo]).insert(box(xa, ya, 0.2))
                for n in path:
                    sh(ZL[n[0]]).insert(box(*self.xy(*n[1:]), NODE[ZL[n[0]]]))
        for net in labels:
            node = next(n for p in self.routes.get(net, []) for n in p) if self.routes.get(net) \
                else next(iter(self.pins[net][0]))
            x, y = self.xy(*node[1:])
            self.top.shapes(self.layout.layer(*LABEL[ZL[node[0]]])).insert(
                kdb.Text(net, kdb.Trans(kdb.Point(d(x), d(y)))))
