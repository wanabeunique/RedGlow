import Xmark from "@/components/SVG/Xmark";
import removeFriend from "../../../api/removeFriend";
import sendFriendRequest from "../../../api/sendFriendRequest";
import styles from "./Friend.module.sass";
import AddFriend from "@/components/SVG/AddFriend";
import RemoveFriend from "@/components/SVG/RemoveFriend";
import Chat from "@/components/SVG/Chat";
import { Link } from "react-router-dom";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { useAppDispatch } from "@/hooks";
import { addFriendCurrent, addFriendOut, removeFriendCurrent, removeFriendIn, removeFriendOut } from "@/store/reducers/friendsSlice";
import { sendNotificationFriend } from "@/socket/friendsSocket";

interface IFriendProps {
  username: string;
  avatar: any;
  type: "current" | "in" | "out" | "search";
}




export default function Friend({ username, type, avatar }: IFriendProps) {
  const dispatch = useAppDispatch() 
     
  async function HandleAccept(nickname: string) {
    const res = await sendFriendRequest(nickname);
    if (res?.status == 201){
      dispatch(addFriendOut(nickname))
      sendNotificationFriend('invite', nickname)
    }
    if (res?.status == 202){
        dispatch(removeFriendIn(nickname))
        dispatch(addFriendCurrent(nickname))
        sendNotificationFriend('accept', nickname)
      }
    }

  async function HandleRemove(nickname: string) {
    const res = await removeFriend(nickname);
    if (res?.status == 200){
      dispatch(removeFriendOut(nickname))
    } 
    if (res?.status == 202){
      dispatch(removeFriendCurrent(nickname))
    } 
  } 
  
  function renderSwitch({ type, username }: IFriendProps) {
    switch (type) {
      // Текущие друзья
      case "current":
        return (
          <div className={styles.tools}>
            <div className={styles.item}>
              <Chat />
            </div>
            <div className={styles.item}>
              <AlertDialog>
                <AlertDialogTrigger>
                  <RemoveFriend />
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
                        HandleRemove(username);
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

      case "in":
        // Входяшие
        return (
          <div className={styles.tools}>
            <div
              className={styles.item}
              onClick={() => {
                HandleAccept(username);
              }}
            >
              <AddFriend />
            </div>
            <div
              className={styles.item}
              onClick={() => {
                HandleRemove(username);
              }}
            >
              <RemoveFriend />
            </div>
          </div>
        );

      case "out":
        // Исходящие
        return (
          <div className={styles.tools}>
            <div
              className={styles.item}
              onClick={() => {
                const res = HandleRemove(username);
              }}
            >
              <Xmark />
            </div>
          </div>
        );

      case "search":
        // Друзья в поиске
        return (
          <div className={styles.tools}>
            <div
              className={styles.item}
              onClick={() => {
                HandleAccept(username);
              }}
            >
              <AddFriend />
            </div>
          </div>
        );

      default:
        return null;
    }
}

  return (
    <div className={styles.wrapper}>
      {avatar ? (
        <p>аватар</p>
      ) : (
        <svg
          className={styles.svg}
          width="25px"
          height="25px"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            opacity="0.1"
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M3 12C3 4.5885 4.5885 3 12 3C19.4115 3 21 4.5885 21 12C21 16.3106 20.4627 18.6515 18.5549 19.8557L18.2395 18.878C17.9043 17.6699 17.2931 16.8681 16.262 16.3834C15.2532 15.9092 13.8644 15.75 12 15.75C10.134 15.75 8.74481 15.922 7.73554 16.4097C6.70593 16.9073 6.09582 17.7207 5.7608 18.927L5.45019 19.8589C3.53829 18.6556 3 16.3144 3 12ZM8.75 10C8.75 8.20507 10.2051 6.75 12 6.75C13.7949 6.75 15.25 8.20507 15.25 10C15.25 11.7949 13.7949 13.25 12 13.25C10.2051 13.25 8.75 11.7949 8.75 10Z"
            fill="white"
          />
          <path
            d="M3 12C3 4.5885 4.5885 3 12 3C19.4115 3 21 4.5885 21 12C21 19.4115 19.4115 21 12 21C4.5885 21 3 19.4115 3 12Z"
            stroke="white"
            stroke-width="2"
          />
          <path d="M15 10C15 11.6569 13.6569 13 12 13C10.3431 13 9 11.6569 9 10C9 8.34315 10.3431 7 12 7C13.6569 7 15 8.34315 15 10Z"
            stroke="white"
            stroke-width="2"
          />
          <path
            d="M6 19C6.63819 16.6928 8.27998 16 12 16C15.72 16 17.3618 16.6425 18 18.9497"
            stroke="white"
            stroke-width="2"
            stroke-linecap="round"
          />
        </svg>
      )}
      <Link to={`/profile/${username}`} className={styles.nickname}>{username}</Link>
      {renderSwitch({ type, username, avatar })}
    </div>
  );
}
