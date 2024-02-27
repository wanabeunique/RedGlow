import { useEffect } from "react";
import Counter from "../Counter/Counter";
import { useAppSelector } from "@/hooks/useAppSelector";

export default function GameAccept() {
  const timeToAccept = useAppSelector((state) => state.gameAcceptReducer.timeToAccept)

  useEffect(() => {
    const audio = new Audio('matchAccept.mp3')
    audio.play()
  }, [])

  return (
    <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-background border border-primary p-10 rounded flex gap-5 flex-col place-items-center w-1/4">
      <p className="text-3xl">Игра найдена</p>
      <p><Counter initialValue={timeToAccept} direction={false} /></p>
      <button className="text-2xl p-3 rounded bg-green-500 hover:scale-105 transition w-full">Принять</button>
    </div>
  );
}
