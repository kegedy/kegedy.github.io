import {useEffect, useState} from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';

const MODEL_VIEWER =
  'https://cdn.jsdelivr.net/npm/@google/model-viewer@3.5.0/dist/model-viewer.min.js';

// Load the <model-viewer> web component once, only on pages that use it
function loadModelViewer() {
  if (document.querySelector(`script[src="${MODEL_VIEWER}"]`)) return;
  const script = document.createElement('script');
  script.type = 'module';
  script.src = MODEL_VIEWER;
  document.head.appendChild(script);
}

const legendStyle = {
  position: 'absolute',
  top: 10,
  right: 10,
  padding: '6px 10px',
  background: 'rgba(0, 0, 0, 0.6)',
  color: '#eee',
  borderRadius: 6,
  fontSize: '0.75rem',
  lineHeight: 1.6,
  pointerEvents: 'none',
};

function Legend({layers, position}) {
  return (
    <div
      style={{
        ...legendStyle,
        ...position,
        display: 'grid',
        gridTemplateColumns: 'auto auto auto',
        alignItems: 'center',
        columnGap: 8,
      }}
      aria-label="Layer legend">
      {layers.map((l) => [
        <span
          key={`${l.name}-swatch`}
          style={{width: 12, height: 12, borderRadius: 2, background: l.color}}
        />,
        <span key={`${l.name}-name`}>{l.name}</span>,
        <span
          key={`${l.name}-range`}
          style={{opacity: 0.6, textAlign: 'right', fontVariantNumeric: 'tabular-nums'}}>
          {l.zmin.toFixed(2)} – {l.zmax.toFixed(2)} µm
        </span>,
      ])}
    </div>
  );
}

export const CAPTION_3D =
  '3D view: drag to rotate, scroll to zoom, right-drag to pan. Layer heights are to scale.';

/**
 * The 3D model with its legend, without figure/caption (also used by LayoutViewer's 3D mode).
 * `legendPosition` overrides the legend's top/right offsets.
 */
export function Model3D({model, height = 450, legendPosition}) {
  const src = useBaseUrl(`/models/${model}`);
  const legendUrl = useBaseUrl(`/models/${model.replace(/\.glb$/, '.json')}`);
  const [legend, setLegend] = useState([]);

  useEffect(loadModelViewer, []);
  useEffect(() => {
    fetch(legendUrl)
      .then((r) => (r.ok ? r.json() : []))
      .then(setLegend)
      .catch(() => setLegend([]));
  }, [legendUrl]);

  return (
    <div style={{position: 'relative'}}>
      <model-viewer
        src={src}
        alt={`3D view of ${model}`}
        camera-controls=""
        orientation="0deg -90deg 0deg"
        camera-orbit="-30deg 55deg 10m"
        shadow-intensity="0"
        exposure="1.1"
        interaction-prompt="none"
        style={{
          display: 'block',
          width: '100%',
          height,
          background: '#111',
          border: '1px solid var(--ifm-color-emphasis-300)',
          borderRadius: 8,
        }}
      />
      {legend.length > 0 && <Legend layers={legend} position={legendPosition} />}
    </div>
  );
}

/**
 * Interactive 3D view of a layout exported by scripts/gds3d.py
 * (static/models/<name>.glb, with its legend in <name>.json).
 *
 *   <LayoutViewer3D model="inverter.glb" />
 *
 * To show 2D and 3D in one viewer with a toggle, use <LayoutViewer file=… model=…> instead.
 */
export default function LayoutViewer3D({model, height = 450}) {
  return (
    <figure style={{margin: '1.5rem 0'}}>
      <Model3D model={model} height={height} />
      <figcaption style={{fontSize: '0.85rem', opacity: 0.8}}>{CAPTION_3D}</figcaption>
    </figure>
  );
}
