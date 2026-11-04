import {useEffect, useRef, useState} from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';

const GREY = '#808080'; // matches the layout viewer's buttons
const ZOOM_STEP = 1.2;
const MAX_ZOOM = 20; // relative to fit
const MIN_ZOOM = 0.5;

const buttonStyle = {
  width: 36,
  height: 31,
  padding: 0,
  fontSize: 14,
  fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
  color: '#000',
  background: GREY,
  border: `1px solid ${GREY}`,
  borderRadius: 4,
  cursor: 'pointer',
};

// Bounding box of the drawing in svg units, ignoring xschem's full-page background rect.
// Measured on screen so text transforms count; null if not laid out (e.g. in a hidden tab).
function contentBox(svg) {
  const inv = svg.getScreenCTM()?.inverse();
  if (!inv) return null;
  let [x1, y1, x2, y2] = [Infinity, Infinity, -Infinity, -Infinity];
  for (const el of svg.querySelectorAll('path, line, text, circle, ellipse, polygon, polyline, rect')) {
    if (el.matches('rect.l0')) continue; // background
    const r = el.getBoundingClientRect();
    if (!r.width && !r.height) continue;
    for (const [cx, cy] of [[r.left, r.top], [r.right, r.bottom]]) {
      const p = new DOMPoint(cx, cy).matrixTransform(inv);
      [x1, y1, x2, y2] = [Math.min(x1, p.x), Math.min(y1, p.y), Math.max(x2, p.x), Math.max(y2, p.y)];
    }
  }
  if (!Number.isFinite(x1)) return null;
  const pad = 0.05 * Math.max(x2 - x1, y2 - y1);
  return [x1 - pad, y1 - pad, x2 - x1 + 2 * pad, y2 - y1 + 2 * pad];
}

/**
 * Zoomable schematic exported by scripts/schematic_svg.sh (static/schematics/<file>).
 * The SVG is inlined and zoomed through its viewBox, so it stays sharp at any zoom.
 *
 *   <SchematicViewer file="inverter.svg" />
 */
export default function SchematicViewer({file, height = 400}) {
  const url = useBaseUrl(`/schematics/${file}`);
  const hostRef = useRef(null);
  const svgRef = useRef(null);
  const homeRef = useRef(null); // viewBox at "fit": [x, y, w, h]
  const [error, setError] = useState(false);

  const getViewBox = () => {
    const v = svgRef.current.viewBox.baseVal;
    return [v.x, v.y, v.width, v.height];
  };
  const setViewBox = (vb) => svgRef.current.setAttribute('viewBox', vb.join(' '));
  const toSvgPoint = (clientX, clientY) =>
    new DOMPoint(clientX, clientY).matrixTransform(svgRef.current.getScreenCTM().inverse());

  // factor > 1 zooms in, keeping svg point (cx, cy) under the same screen position
  const zoomAt = (factor, cx, cy) => {
    const [x, y, w, h] = getViewBox();
    const zoom = homeRef.current[2] / (w / factor);
    if (zoom > MAX_ZOOM || zoom < MIN_ZOOM) return;
    setViewBox([cx - (cx - x) / factor, cy - (cy - y) / factor, w / factor, h / factor]);
  };
  const zoomCenter = (factor) => {
    if (!svgRef.current) return;
    const [x, y, w, h] = getViewBox();
    zoomAt(factor, x + w / 2, y + h / 2);
  };
  const fit = () => {
    if (!svgRef.current) return;
    // Fit to the drawing; measure now if it was hidden when it loaded
    if (!homeRef.current.tight) {
      const box = contentBox(svgRef.current);
      if (box) homeRef.current = Object.assign(box, {tight: true});
    }
    setViewBox(homeRef.current);
  };

  // Load the SVG and inline it (our own static file)
  useEffect(() => {
    let cancelled = false;
    fetch(url)
      .then((r) => {
        if (!r.ok) throw new Error(`${r.status}`);
        return r.text();
      })
      .then((text) => {
        if (cancelled) return;
        const host = hostRef.current;
        host.innerHTML = text;
        const svg = host.querySelector('svg');
        svg.style.width = '100%';
        svg.style.height = '100%';
        svg.style.display = 'block';
        svgRef.current = svg;
        homeRef.current = getViewBox();
        fit();
      })
      .catch(() => !cancelled && setError(true));
    return () => {
      cancelled = true;
    };
  }, [url]);

  // Wheel zoom (non-passive so the page doesn't scroll) and drag to pan
  useEffect(() => {
    const host = hostRef.current;
    let drag = null;

    const onWheel = (e) => {
      if (!svgRef.current) return;
      e.preventDefault();
      const p = toSvgPoint(e.clientX, e.clientY);
      zoomAt(e.deltaY < 0 ? ZOOM_STEP : 1 / ZOOM_STEP, p.x, p.y);
    };
    const onPointerDown = (e) => {
      if (!svgRef.current || e.button !== 0) return;
      host.setPointerCapture(e.pointerId);
      drag = {x: e.clientX, y: e.clientY, vb: getViewBox(), scale: svgRef.current.getScreenCTM().a};
      host.style.cursor = 'grabbing';
    };
    const onPointerMove = (e) => {
      if (!drag) return;
      const [x, y, w, h] = drag.vb;
      setViewBox([
        x - (e.clientX - drag.x) / drag.scale,
        y - (e.clientY - drag.y) / drag.scale,
        w,
        h,
      ]);
    };
    const onPointerUp = () => {
      drag = null;
      host.style.cursor = 'grab';
    };

    host.addEventListener('wheel', onWheel, {passive: false});
    host.addEventListener('pointerdown', onPointerDown);
    host.addEventListener('pointermove', onPointerMove);
    host.addEventListener('pointerup', onPointerUp);
    host.addEventListener('pointercancel', onPointerUp);
    host.addEventListener('dblclick', fit);
    return () => {
      host.removeEventListener('wheel', onWheel);
      host.removeEventListener('pointerdown', onPointerDown);
      host.removeEventListener('pointermove', onPointerMove);
      host.removeEventListener('pointerup', onPointerUp);
      host.removeEventListener('pointercancel', onPointerUp);
      host.removeEventListener('dblclick', fit);
    };
  }, []);

  return (
    <figure style={{margin: '1.5rem 0'}}>
      <div
        style={{
          position: 'relative',
          height,
          background: '#000',
          border: '1px solid var(--ifm-color-emphasis-300)',
          borderRadius: 8,
          overflow: 'hidden',
        }}>
        <div
          ref={hostRef}
          role="img"
          aria-label={`Schematic: ${file}`}
          style={{width: '100%', height: '100%', cursor: 'grab', touchAction: 'none'}}
        />
        {error && (
          <div style={{position: 'absolute', inset: 0, display: 'grid', placeItems: 'center', color: '#ccc'}}>
            Couldn't load {file}
          </div>
        )}
        <div
          style={{
            position: 'absolute',
            top: 12,
            right: 12,
            display: 'flex',
            flexDirection: 'column',
            gap: 8,
          }}>
          <button type="button" style={buttonStyle} onClick={() => zoomCenter(ZOOM_STEP)} aria-label="Zoom in" title="Zoom in">
            +
          </button>
          <button type="button" style={buttonStyle} onClick={() => zoomCenter(1 / ZOOM_STEP)} aria-label="Zoom out" title="Zoom out">
            −
          </button>
          <button type="button" style={buttonStyle} onClick={fit} aria-label="Fit to view" title="Fit to view">
            Fit
          </button>
        </div>
      </div>
    </figure>
  );
}
