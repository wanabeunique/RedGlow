import ChangeProfileBg from '@/components/Profile/ProfileChangeBg';
import ChangeProfilePhoto from '@/components/Profile/ProfileChangePhoto';
import { useEffect, useState } from 'react';
import { useAppSelector } from '@/hooks/useAppSelector';
import { IDate } from '@/functions/parseDate';
import defaultBg from '@/assets/profile-bg.png';
import defaultAvatar from '@/assets/profile-photo.png';
import parseDate from '@/functions/parseDate';

export default function ProfileTop({ user, isOwnProfile }) {
  const userPhoto = useAppSelector((store) => store.userReducer.photo);
  const [userBackground, setUserBackground] = useState<string>();
  const [parsedDate, setParsedDate] = useState<IDate>();

  useEffect(() => {
    if (!user) {
      return;
    }
    setParsedDate(parseDate(user.date_joined));
  }, [user]);

  console.log(user);
  return (
    <div className="relative">
      <img
        src={userBackground || defaultBg}
        className="w-full h-[50vh] object-cover"
      />
      {isOwnProfile && <ChangeProfileBg />}
      <div className="container w-full absolute top-1/2 -translate-y-1/2 ">
        <div className="flex place-items-center gap-2 bg-[rgba(0,0,0,0.75)] w-max p-7 rounded-xl">
          <div className="relative">
            <img
              className="rounded-full w-[256px] h-[256px]"
              src={userPhoto || defaultAvatar}
            />
            {isOwnProfile && <ChangeProfilePhoto />}
          </div>
          <div className="flex flex-col gap-3">
            <p className="text-3xl text-white font-bold">
              {user ? user.username : null}
            </p>
            <p className="text-xl font-light">
              На сайте с {parsedDate?.day} {parsedDate?.month}{' '}
              {parsedDate?.year}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
