import { useState, useEffect } from "react";
import { Progress } from '@/components/ui/progress';

export default function ProfileStats({ user }) {
  const [decency, setDecency] = useState(0);
  const [reports, setReports] = useState(0);

  useEffect(() => {
    if (user) {
      setDecency(Math.ceil(user.decency / 100));
      setReports(user.reports);
    }
  }, [user]);

  return (
    <div className="flex flex-col w-full gap-5 mt-5">
      <p className="text-3xl">Статистика</p>
      <div className="flex flex-col gap-4">
        <p>Порядочность: {user?.decency} из 1000 </p>
        <Progress value={decency} />
      </div>
      <div className="flex flex-col mt-2 gap-4">
        <p>
          На вас было оставлено {reports} жалоб, осталось еще {100 - reports} до
          временной блокировки{' '}
        </p>
        <Progress value={reports} />
      </div>
    </div>
  );
}
