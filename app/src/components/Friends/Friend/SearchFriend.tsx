import friendsSocket from '@/socket/friendsSocket';
import styles from './Friend.module.sass'
import { faUserPlus } from '@fortawesome/free-solid-svg-icons';
import {
  FontAwesomeIcon,
} from '@fortawesome/react-fontawesome';
import { useAppDispatch } from '@/hooks/useAppDispatch';
import { createInvite } from '@/store/reducers/friendsSlice';

export default function SearchFriend({username}: string) {
  const dispatch = useAppDispatch()
  return (
    <div className={styles.tools}>
      <div
        className={styles.item}
        onClick={() => {
          friendsSocket.sendFriendEvent('create_invite', username);
          dispatch(createInvite(username))
        }}
      >
        <FontAwesomeIcon icon={faUserPlus} />
      </div>
    </div>
  );
}
