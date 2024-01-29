import styles from './Friend.module.sass';
import { Link } from 'react-router-dom';
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from '@/components/ui/hover-card';
import { useState } from 'react';
import parseDate, { IDate } from '@/functions/parseDate';
import userService from '@/service/user.service';
import CurrentFriend from './CurrentFriend';
import InviteFriend from './InviteFriend';
import RequestFriend from './RequestFriend';
import SearchFriend from './SearchFriend';
import { faUserLarge } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

interface IFriendProps {
  username: string;
  avatar: any;
  type: 'current' | 'in' | 'out' | 'search';
}

export default function Friend({ username, type, avatar }: IFriendProps) {
  const [parsedDate, setParsedDate] = useState<IDate>();
  const [flagUserProfile, setFlagUserProfile] = useState<boolean>(true);
  const [userBg, setUserBg] = useState<string>();

  async function getModal(nickname: string) {
    if (!flagUserProfile) return;
    const response = await userService.getUserProfile(nickname);
    const parsedDate = parseDate(response.date_joined);
    setParsedDate(parsedDate);
    setFlagUserProfile(false);
    const bg = await userService.getUserBackground(response.username);
    setUserBg(bg);
  }

  function renderSwitch({ type, username }: IFriendProps) {
    switch (type) {
      // Текущие друзья
      case 'current':
        return (
          <CurrentFriend username={username}  />  
        );

      case 'in':
        // Входяшие
        return (
         <InviteFriend username={username} /> 
        );

      case 'out':
        // Исходящие
        return (
          <RequestFriend username={username}/> 
        );

      case 'search':
        // Друзья в поиске
        return (
          <SearchFriend username={username}/> 
        );

      default:
        return null;
    }
  }
  return (
    <HoverCard openDelay={100}>
      <HoverCardTrigger>
        <Link
          to={`/profile/${username}`}
          onMouseEnter={() => {
            getModal(username);
          }}
          className="flex items-center gap-2 rounded border p-2"
        >
          {avatar ? (
            <img
              src={`${import.meta.env.VITE_API_SERVER}/media/${avatar}`}
              className={styles.avatar}
            />
          ) : (
            <FontAwesomeIcon icon={faUserLarge} />
          )}
          <p className={styles.nickname_preview}>{username}</p>
        </Link>
      </HoverCardTrigger>
      <HoverCardContent className={styles.modal}>
        <img className={styles.modal__bg} src={userBg} />
        <div className={styles.modal__content}>
          <div className={styles.modal__info}>
            <Link to={`/profile/${username}`} className={styles.modal__wrapper}>
              {avatar ? (
                <img
                  src={`${import.meta.env.VITE_API_SERVER}/media/${avatar}`}
                  className={styles.avatar}
                />
              ) : (
                <FontAwesomeIcon icon={faUserLarge} />
              )}
              <p className={styles.nickname}>{username}</p>
            </Link>
          </div>
          <div className={styles.modal__bottom}>
            {renderSwitch({ type, username, avatar })}
            {parsedDate && (
              <p>
                На сайте с {parsedDate.day} {parsedDate.month} {parsedDate.year}
              </p>
            )}
          </div>
        </div>
      </HoverCardContent>
    </HoverCard>
  );
}
