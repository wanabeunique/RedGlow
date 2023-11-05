import ArrowLeft from '../SVG/ArrowLeft';
import ArrowRight from '../SVG/ArrowRight';
import styles from './Pagination.module.sass';

interface IPagination {
  page: number;
  next: boolean;
  setPage: ReactState;
}

export default function Pagination({ page, next, setPage }: IPagination) {
  return (
    <div className={styles.wrapper}>
      <button
        disabled={page == 1}
        onClick={() => {
          setPage((prev) => prev - 1);
        }}
        className={`${styles.item} ${page == 1 ? styles.disabled : null}`}
      >
        <ArrowLeft />
      </button>
      <div className={styles.item}>{page}</div>
      <button
        disabled={!next}
        onClick={() => {
          setPage((prev) => prev + 1);
        }}
        className={`${styles.item} ${!next ? styles.disabled : null}`}
      >
        <ArrowRight />
      </button>
    </div>
  );
}
