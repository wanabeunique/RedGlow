import styles from './Proflie.module.sass';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useAppSelector } from '@/hooks/useAppSelector';
import { useNavigate } from 'react-router-dom';
import { IOwnProfile } from '@/interfaces/IOwnProfile';
import parseDate from '@/functions/parseDate';
import userService from '@/service/user.service';
import ProfileFriends from '@/components/Profile/ProfileFriends';
import ProfileStats from '@/components/Profile/ProfileStats';
import ProfileSettingsLink from './ProfileSettingsLink';
import ProfileTop from './ProfileTop';

export default function Profile() {
  const navigate = useNavigate();
  const { searchName } = useParams<{ searchName: string }>();
  const username = useAppSelector((state) => state.userReducer.username);
  
  const [user, setUser] = useState<IOwnProfile>();

  const isOwnProfile = searchName == username;

  useEffect(() => {
    const getUser = async () => {
      if (isOwnProfile) {
        const userData = await userService.getProfile();
        setUser(userData);
        const parsedDate = parseDate(userData.date_joined);
        const userBackground = await userService.getUserBackground(
          userData.username,
        );
        setUserBackground(userBackground);
      } else {
        const user = await userService.getUserProfile(searchName);
        if (!user) {
          return navigate('/');
        }
        setUser(user);
        const userBackground = await userService.getUserBackground(
          user.username,
        );
        setUserBackground(userBackground);
        const photo = await userService.getUserPhoto(user.username);
      }
    };
    getUser();
  }, [searchName]);

  console.log(user);

  return (
    <div className={`${styles.profile}`}>
      <ProfileTop user={user} isOwnProfile={isOwnProfile}/> 
      <div
        className={`container ${styles.profile__content} grid grid-cols-6 gap-10`}
      >
        <div className={`${styles.profile__left} col-span-4 `}>
          <p className="mt-10">История игр</p>
          <ProfileStats user={user} />
        </div>
        <div>
          {isOwnProfile && <ProfileSettingsLink />}
          <ProfileFriends user={user} />
        </div>
      </div>
    </div>
  );
}
