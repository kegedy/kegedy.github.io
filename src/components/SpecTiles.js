import styles from './SpecTiles.module.css';

/**
 * A row of summary tiles: a short label, a large value, and an optional note.
 *
 *   <SpecTiles tiles={[{label: 'Process', value: 'sky130', note: '130 nm'}]} />
 */
export default function SpecTiles({tiles}) {
  return (
    <div className={styles.row}>
      {tiles.map(({label, value, note}) => (
        <div className={styles.tile} key={label}>
          <div className={styles.label}>{label}</div>
          <div className={styles.value}>{value}</div>
          {note && <div className={styles.note}>{note}</div>}
        </div>
      ))}
    </div>
  );
}
