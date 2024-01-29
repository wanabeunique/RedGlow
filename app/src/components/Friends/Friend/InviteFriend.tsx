import friendsSocket from '@/socket/friendsSocket';
import styles from './Friend.module.sass';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUserPlus, faUserMinus } from '@fortawesome/free-solid-svg-icons';
import { useAppDispatch } from '@/hooks/useAppDispatch';
import { acceptInvite, cancelInvite } from '@/store/reducers/friendsSlice';

export default function InviteFriend({ username }: string) {
  const dispatch = useAppDispatch()
  return (
    <div className={styles.tools}>
      <div
        className={styles.item}
        onClick={() => {
          friendsSocket.sendFriendEvent('accept_invite', username);
          dispatch(acceptInvite(username))
        }}
      >
        <FontAwesomeIcon icon={faUserPlus} />
      </div>
      <div
        className={styles.item}
        onClick={() => {
          friendsSocket.sendFriendEvent('decline_invite', username);
          dispatch(cancelInvite(username));
        }}
      >
        <FontAwesomeIcon icon={faUserMinus} />
      </div>
    </div>
  );
}
