import {useEffect, useState} from 'react';

const fullscreenElement = () => document.fullscreenElement || document.webkitFullscreenElement;

/**
 * Full-screen toggle for the element in `ref`.
 * `supported` is false where the browser can't put an element in full screen (e.g. iPhone Safari),
 * so callers can hide the button.
 */
export function useFullscreen(ref) {
  const [active, setActive] = useState(false);
  const [supported, setSupported] = useState(false);

  useEffect(() => {
    setSupported(Boolean(document.fullscreenEnabled || document.webkitFullscreenEnabled));
    const onChange = () => setActive(Boolean(ref.current) && fullscreenElement() === ref.current);
    document.addEventListener('fullscreenchange', onChange);
    document.addEventListener('webkitfullscreenchange', onChange);
    return () => {
      document.removeEventListener('fullscreenchange', onChange);
      document.removeEventListener('webkitfullscreenchange', onChange);
    };
  }, [ref]);

  const toggle = () => {
    const el = ref.current;
    if (!el) return;
    const call = fullscreenElement()
      ? (document.exitFullscreen || document.webkitExitFullscreen)?.call(document)
      : (el.requestFullscreen || el.webkitRequestFullscreen)?.call(el);
    Promise.resolve(call).catch(() => {});
  };

  return {active, supported, toggle};
}

/** Four-corner full-screen icon; shows the "exit" version while `active`. */
export function FullscreenIcon({active, size = 16}) {
  const d = active
    ? 'M9 4v5H4M15 4v5h5M15 20v-5h5M9 20v-5H4'
    : 'M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5';
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      style={{display: 'block', margin: 'auto'}}>
      <path d={d} />
    </svg>
  );
}
