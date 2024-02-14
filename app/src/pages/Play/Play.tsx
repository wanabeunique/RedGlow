import ChooseGame from '@/components/Play/ChooseGame';
import StartGame from '@/components/Play/StartGame';

export default function Play() {
  return (
    <div>
      <div className="border-b p-5">
        <div className="container flex place-items-center justify-between">
            <ChooseGame />
            <StartGame />
        </div>
      </div>
    </div>
  );
}
