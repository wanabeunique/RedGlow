import { useAppSelector } from '@/hooks/useAppSelector';
import Counter from '../Counter/Counter';
import { faXmark } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { useAppDispatch } from '@/hooks/useAppDispatch';
import { stopSearch } from '@/store/reducers/gameSlice';

export default function Search() {
  const dispatch = useAppDispatch();
  

  return (
    <div>
      <div className="fixed right-10 bottom-10 border rounded p-4 border-primary text-l flex place-items-center">
        Поиск игроков...
        <span>&nbsp;</span>
        <Counter />
        <button
          onClick={() => {
            dispatch(stopSearch());
          }}
          className="ml-3 border p-2 rounded hover:border-primary transition"
        >
          <FontAwesomeIcon icon={faXmark} />
        </button>
      </div>
    </div>
  );
}
