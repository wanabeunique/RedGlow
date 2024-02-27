import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUserGroup } from '@fortawesome/free-solid-svg-icons';
import styles from '@/pages/Profile/Proflie.module.sass';
import Friend from '../Friends/Friend/Friend';
import { useEffect, useState } from 'react';
import friendsService from '@/service/friends.service';

export default function ProfileFriends({ user }) {
  const [friendsCurrentPage, setFriendsCurrentPage] = useState<number>(1);
  const [friendsData, setFriendsData] = useState<any>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (user) {
      const HandleFriends = async () => {
        const friendsDataValue: Array<string> =
          await friendsService.getUserFriends(
            user.username,
            friendsCurrentPage,
          );
        setFriendsData(friendsDataValue);
      };
      HandleFriends();
    }
    setIsLoading(false);
  }, [user]);

  if (!friendsData.length) {
    return (
      <p
        className={styles.friends__text}
      >{`У вас пока что нет ни одного друга, но не стоит расстраиваться...`}</p>
    );
  }

  return (
    <div className="mt-10 ">
      <div className="flex items-center gap-2 ">
        <FontAwesomeIcon icon={faUserGroup} />
        <p className={`${styles.friends__title}`}>Список друзей:</p>
      </div>
      <div className="flex flex-col gap-2 mt-5">
        {friendsData.map((friend: any) => (
          <Friend
            username={friend.username}
            type="current"
            avatar={friend.photo}
          />
        ))}
      </div>
    </div>
  );
}
