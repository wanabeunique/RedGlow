import * as React from 'react';
import { Check, ChevronsUpDown } from 'lucide-react';

import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from '@/components/ui/command';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { useAppSelector } from '@/hooks/useAppSelector';
import { useAppDispatch } from '@/hooks/useAppDispatch';
import { setSelectedGame } from '@/store/reducers/gameSlice';

const games = [
  {
    value: 'civilization5',
    label: 'Сivilization 5',
  },
  {
    value: 'civilization6',
    label: 'Civilization 6',
  },
];

export default function ChooseGame() {
  const [open, setOpen] = React.useState(false);
  const value = useAppSelector((state) => state.gameReducer.selectedGame)
  const dispatch = useAppDispatch()

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-[200px] justify-between"
        >
          {value
            ? games.find((game) => game.value === value)?.label
            : 'Выберите игру...'}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandInput placeholder="Поиск игры..." />
          <CommandEmpty>Игра не найдена</CommandEmpty>
          <CommandGroup>
            {games.map((game) => (
              <CommandItem
                key={game.value}
                value={game.value}
                onSelect={(currentValue) => {
                  dispatch(setSelectedGame(currentValue === value ? '' : currentValue));
                  setOpen(false);
                }}
              >
                <Check
                  className={cn(
                    'mr-2 h-4 w-4',
                    value === game.value ? 'opacity-100' : 'opacity-0',
                  )}
                />
                {game.label}
              </CommandItem>
            ))}
          </CommandGroup>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
