import styles from './Proflie.module.sass';
import { useEffect, useState } from 'react';
import defaultAvatar from '@/assets/profile-photo.png';
import defaultBg from '@/assets/profile-bg.png';
import IProfile from '@/interfaces/IProfile';
import { IDate } from '@/functions/parseDate';
import Friend from '@/components/Friends/Friend/Friend';

interface IUserProfile {
  username: string;
}

export default function UserProfile({ username }: IUserProfile) {
  const [friendsData, setFriendsData] = useState<any>([]);
  const [user, setUser] = useState<IProfile>();
  const [parsedDate, setParsedDate] = useState<IDate>();
  const [userBackground, setUserBackground] = useState<string>();
  const [userPhoto, setUserPhoto] = useState<string>();

  useEffect(() => {
    async function fetchUser() {
      
    }
    fetchUser();
  }, [navigate]);
  return (
    <div className={`${styles.profile}`}>
      <div className={styles.profile__top}>
        <img
          className={styles.profile__top_bg}
          src={userBackground || defaultBg}
          alt=""
        />
        <div className="container">
          <div className={`${styles.profile__top_wrapper} `}>
            <div className={styles.profile__top_avatar}>
              <img
                className={styles.user__photo}
                src={userPhoto || defaultAvatar}
              />
            </div>
            <div className={styles.profile__top_text}>
              <p className={`${styles.profile__top_nickname} title`}>
                {user ? <span>{user.username}</span> : null}
              </p>
              <p className={`${styles.profile__top_registratedTime} text`}>
                На сайте с {parsedDate?.day} {parsedDate?.month}{' '}
                {parsedDate?.year}
              </p>
            </div>
          </div>
        </div>
      </div>
      <div
        className={`container ${styles.profile__content} grid grid-cols-6 gap-10`}
      >
        <div className={`${styles.profile__left} col-span-4 `}>
          <p>История игр</p>
        </div>
        <div className={styles.profile__right}>
          <p className={`mt-10 ${styles.friends__title}`}>Друзья:</p>
          {friendsData.length > 0 ? (
            <div className={`${styles.friends__items} mt-5`}>
              {friendsData.map((friend: any) => (
                <Friend
                  username={friend.username}
                  type="current"
                  avatar={friend.photo}
                />
              ))}
            </div>
          ) : (
            <p className={styles.friends__text}>
              У {user?.username} пока что нет ни одного друга
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
