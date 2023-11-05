import Xmark from "@/components/SVG/Xmark";
import getUserBackground from "@/api/getUserBackground";
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
import Avatar from "@/components/SVG/Avatar";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card"
import getUserProfile from "@/api/getUserProfile";
import { useEffect, useState } from "react";
import IProfile from "@/interfaces/IProfile";
import parseDate, { IDate } from "@/functions/parseDate";


interface IFriendProps {
  username: string;
  avatar: any;
  type: "current" | "in" | "out" | "search";
}

export default function Friend({ username, type, avatar }: IFriendProps) {
  const [userData, setUserData] = useState<IProfile>()
  const [parsedDate, setParsedDate] = useState<IDate>()
  const [flagUserProfile, setFlagUserProfile] = useState<boolean>(true)
  const [userBg, setUserBg] = useState<string>()
  const dispatch = useAppDispatch() 

  async function getModal(nickname: string){
    if (!flagUserProfile) return
    const response = await getUserProfile(nickname)
    setUserData(response)
    const parsedDate = parseDate(response.date_joined)
    setParsedDate(parsedDate)
    setFlagUserProfile(false)
    const bg = await getUserBackground(response.username)
    setUserBg(bg)
  }

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
      dispatch(removeFriendIn(nickname))
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
    <HoverCard>
      <HoverCardTrigger>
        <Link 
          to={`/profile/${username}`} 
          onMouseEnter={() => {getModal(username)}}
          className={styles.wrapper}
        >
          {avatar ? (
            <img src={`${import.meta.env.VITE_API_SERVER}/media/${avatar}`} className={styles.avatar} /> 
          ) : (
            <Avatar /> 
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
                <img src={`${import.meta.env.VITE_API_SERVER}/media/${avatar}`} className={styles.avatar} /> 
              ) : (
                <Avatar /> 
              )}
              <p className={styles.nickname}>{username}</p>
            </Link>
          </div>
          <div className={styles.modal__bottom}>
            {renderSwitch({ type, username, avatar })}
            {parsedDate && (<p>На сайте с {parsedDate.day} {parsedDate.month} {parsedDate.year}</p>)}
          </div> 
        </div> 
      </HoverCardContent>
    </HoverCard>
  );
}


