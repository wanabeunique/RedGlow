import friendsSocket from '@/socket/friendsSocket';
import styles from './Friend.module.sass';
import Xmark from '@/components/SVG/Xmark';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUserXmark} from '@fortawesome/free-solid-svg-icons'

export default function RequestFriend({username}: string) {
  return (
    <div className={styles.tools}>
      <div
        className={styles.item}
        onClick={() => {
          friendsSocket.sendFriendEvent('cancel_invite', username);
        }}
      >
      <FontAwesomeIcon icon={faUserXmark} />  
      </div>
    </div>
  );
}
