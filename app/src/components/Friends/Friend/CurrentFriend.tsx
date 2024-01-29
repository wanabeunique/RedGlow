import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog';
import styles from './Friend.module.sass';
import { faUserMinus, faMessage } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import friendsSocket from '@/socket/friendsSocket';
import { useAppDispatch } from '@/hooks/useAppDispatch';
import { useAppSelector } from '@/hooks/useAppSelector';
import { deleteFriend } from '@/store/reducers/friendsSlice';

export default function CurrentFriend({ username }: string) {
  const dispatch = useAppDispatch();
  console.log(useAppSelector((store) => store.friendsSlice.current));

  return (
    <div className={styles.tools}>
      <div className={styles.item}>
        <FontAwesomeIcon icon={faMessage} />
      </div>
      <div className={`${styles.item}`}>
        <AlertDialog>
          <AlertDialogTrigger className="flex">
            <FontAwesomeIcon icon={faUserMinus} />
          </AlertDialogTrigger>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>
                Вы точно хотите удалить {username} из списка друзей?
              </AlertDialogTitle>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel>Отмена</AlertDialogCancel>
              <AlertDialogAction
                onClick={() => {
                  friendsSocket.sendFriendEvent('delete_friend', username);
                  dispatch(deleteFriend(username));
                }}
              >
                Удалить
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
      </div>
    </div>
  );
}
