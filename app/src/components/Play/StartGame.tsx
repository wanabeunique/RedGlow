import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from '@/components/ui/drawer';
import { Button } from '../ui/button';
import { useAppSelector } from '@/hooks/useAppSelector';
import { useAppDispatch } from '@/hooks/useAppDispatch';
import { setCountPlayers } from '@/store/reducers/gameSlice';
import matchmakingSocket from '@/socket/matchmakingSocket';
import { useEffect, useState } from 'react';

const countPlayers = [2, 4, 8];

export default function StartGame() {
  const dispatch = useAppDispatch();
  const {
    eloFilter,
    selectedGame: game,
    countPlayers: count,
  } = useAppSelector((state) => state.gameReducer);

  const searchRunning = useAppSelector(
    (state) => state.gameReducer.activeSearch,
  );

  const onOptionChange = (e: React.ChangeEvent<any>) => {
    dispatch(setCountPlayers(e.target.value));
  };

  return (
    <Drawer>
      <DrawerTrigger disabled={!game}>
        <Button
          disabled={!game || searchRunning}
          className="rounded bg-green-500 hover:bg-green-600"
        >
          Начать игру
        </Button>
      </DrawerTrigger>
      <DrawerContent>
        <DrawerHeader className="container">
          <DrawerTitle className="text-2xl">
            Выберите количество игроков
          </DrawerTitle>
          <div className="flex place-items-center justify-self-center gap-3">
            {countPlayers.map((count) => (
              <label
                key={count}
                className="flex place-items-center justify-center p-5 cursor-pointer border text-2xl rounded aspect-square w-[70px] hover:bg-accent"
              >
                <span>{count}</span>
                <input
                  hidden
                  type="radio"
                  value={count}
                  name="count"
                  onChange={onOptionChange}
                />
              </label>
            ))}
          </div>
          <span className="text-5xl justify-self-center mt-5 text-primary font-extrabold">
            {count}
          </span>
        </DrawerHeader>
        <DrawerFooter className="container">
          <DrawerClose>
            <Button
              onClick={() => {
                matchmakingSocket.startSearch(Number(count), game, eloFilter);
              }}
              className="rounded w-full"
            >
              Начать поиск
            </Button>
          </DrawerClose>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  );
}
