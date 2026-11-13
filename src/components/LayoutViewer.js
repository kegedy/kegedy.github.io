import {useState} from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {Model3D, CAPTION_3D} from '@site/src/components/LayoutViewer3D';

// Lines up with kweb's Zoom Fit / full-screen column inside the iframe (measured from
// kweb/templates/viewer.html): same right edge and width, mirrored to the top corner.
// Includes the iframe's 1px border.
const CONTROLS_INSET = 21; // px from the viewer's top and right edges
const CONTROLS_WIDTH = 91; // px, width of kweb's button column
const GREY = '#808080'; // kweb's button color

const toggleStyle = {
  position: 'absolute',
  top: CONTROLS_INSET,
  right: CONTROLS_INSET,
  width: CONTROLS_WIDTH,
  zIndex: 1,
  display: 'flex',
};

// Styled like kweb's select/ruler group: active = filled grey, inactive = outlined
function ViewToggle({mode, setMode}) {
  return (
    <div style={toggleStyle} role="group" aria-label="Layout view">
      {['2D', '3D'].map((m, i) => (
        <button
          key={m}
          type="button"
          aria-pressed={mode === m}
          onClick={() => setMode(m)}
          style={{
            flex: 1,
            height: 31,
            padding: '4px 8px',
            fontSize: 14,
            fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
            cursor: 'pointer',
            border: `1px solid ${GREY}`,
            borderRadius: i === 0 ? '4px 0 0 4px' : '0 4px 4px 0',
            color: mode === m ? '#000' : GREY,
            background: mode === m ? GREY : 'rgba(0, 0, 0, 0.6)',
          }}>
          {m}
        </button>
      ))}
    </div>
  );
}

/**
 * Embeds an interactive kweb view of a GDS/OAS file from the gds/ folder.
 *
 *   <LayoutViewer file="inverter.gds" cell="INV" height={500} />
 *
 * `layerProps` names a .lyp file (also in gds/) that gives layers their names
 * and colors. Defaults to sky130A; pass layerProps={null} for raw layer numbers.
 *
 * Pass `model` (a .glb from scripts/gds3d.py) to add a 2D/3D toggle:
 *
 *   <LayoutViewer file="inverter.gds" cell="INV" model="inverter.glb" />
 */
export default function LayoutViewer({
  file,
  cell,
  layerProps = 'sky130A.lyp',
  model,
  height = 600,
}) {
  const {siteConfig} = useDocusaurusContext();
  const base = siteConfig.customFields.kwebUrl;
  const params = new URLSearchParams({file});
  if (cell) params.set('cell', cell);
  if (layerProps) params.set('layer_props', layerProps);
  const src = `${base}/view?${params}`;

  const [mode, setMode] = useState('2D');
  // Mount the 3D view on first use, then keep both mounted so switching back keeps state
  const [shown3D, setShown3D] = useState(false);
  const switchMode = (m) => {
    if (m === '3D') setShown3D(true);
    setMode(m);
  };

  return (
    <figure style={{margin: '1.5rem 0'}}>
      <div style={{position: 'relative'}}>
        {model && <ViewToggle mode={mode} setMode={switchMode} />}
        <iframe
          src={src}
          title={`Layout: ${file}`}
          loading="lazy"
          allow="fullscreen"
          allowFullScreen
          style={{
            display: mode === '2D' ? 'block' : 'none',
            width: '100%',
            height,
            border: '1px solid var(--ifm-color-emphasis-300)',
            borderRadius: 8,
          }}
        />
        {model && shown3D && (
          <div style={{display: mode === '3D' ? 'block' : 'none'}}>
            <Model3D
              model={model}
              height={height}
              legendPosition={{top: CONTROLS_INSET + 31 + 8, right: CONTROLS_INSET}}
              buttonPosition={{bottom: CONTROLS_INSET, right: CONTROLS_INSET, width: CONTROLS_WIDTH}}
            />
          </div>
        )}
      </div>
      <figcaption style={{fontSize: '0.85rem', opacity: 0.8}}>
        {mode === '3D' ? (
          CAPTION_3D
        ) : (
          <>
            Interactive layout: scroll to zoom, drag to pan.{' '}
            <a href={src} target="_blank" rel="noopener noreferrer">
              Open full screen ↗
            </a>{' '}
            (first load may take ~30 s if the viewer is waking up)
          </>
        )}
      </figcaption>
    </figure>
  );
}
