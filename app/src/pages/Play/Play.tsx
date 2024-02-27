import ChooseGame from '@/components/Play/ChooseGame';
import EloFilter from '@/components/Play/EloFilter';
import StartGame from '@/components/Play/StartGame';

export default function Play() {
  return (
    <div>
      <div className="border-b p-5">
        <div className="container flex place-items-center justify-between">
          <div className='flex place-items-center gap-3'>
            <ChooseGame />
            <EloFilter />
          </div>
          <StartGame />
        </div>
      </div>
    </div>
  );
}
