import { useAppSelector } from '@/hooks/useAppSelector';
import { Button } from '../ui/button';
import { useAppDispatch } from '@/hooks/useAppDispatch';
import { toggleEloFilter } from '@/store/reducers/gameSlice';

export default function EloFilter() {
  const dispatch = useAppDispatch();
  const eloFilter = useAppSelector((state) => state.gameReducer.eloFilter);

  console.log(eloFilter);

  return (
    <Button
      className={`hover:scale-105 hover:bg-[none] rounded transition ${eloFilter ? "bg-green-500" : "bg-red-500"}`}
      onClick={() => {
        dispatch(toggleEloFilter());
      }}
    >
      {eloFilter ? (
        <div className="">Фильтр по эло активирован</div>
      ) : (
        <div>Фильтр по эло выключен</div>
      )}
    </Button>
  );
}
