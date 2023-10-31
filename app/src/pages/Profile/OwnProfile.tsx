import styles from "./Proflie.module.sass";
import Avatar from "react-avatar-edit";
import {default as AvatarImg} from "antd/es/avatar/avatar";
import ChangePhoto from "@/components/SVG/ChangePhoto";
import { useState } from "react";
import getProfile from "../../api/getProfile";
import { useEffect } from "react";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import getUserFriends from "@/api/getUserFriends";
import getFriendsRequestIn from "@/api/getFriendsRequestIn";
import Friend from "@/components/Friends/Friend/Friend";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Separator } from "@/components/ui/separator";
import { Input } from "@/components/ui/input";
import changePassword from "@/api/changePassword";
import { Button } from "@/components/ui/button";
import { IOwnProfile } from "@/interfaces/IOwnProfile";
import changePhoto from "@/api/changePhoto";
import base64toFile from "@/functions/base64toFile";
import removeBodyClasses from "@/functions/civilization5/removeBodyClasses";
import { useAppSelector } from "@/hooks";

const lableStyle = {
  color: "hsl(var(--foreground))",
  width: "100%",
  display: "flex",
  alignItems: 'center',
  justifyContent: "center",
  cursor: "pointer"
}  

export default function OwnProfile() {
  const userPhoto = useAppSelector(store => store.userReducer.photo)

  const [friendsInPage, setFriendsInPage] = useState<number>(1)
  const [friendsOutPage, setFriendsOutPage] = useState<number>(1)
  const [friendsCurrentPage, setFriendsCurrentPage] = useState<number>(1)

  
  const [user, setUser] = useState<IOwnProfile>();
  const [decency, setDecency] = useState<number>(0);
  const [reports, setReports] = useState<number>(0);
  const [friendsData, setFriendsData] = useState<any>([]);
  const [friendsInvite, setFriendsInvite] = useState([]);

  const [currentPassword, setCurrentPassword] = useState<any>("");
  const [newPassword, setNewPassword] = useState<any>("");
  const [selectedPhoto,setSelectedPhoto] = useState<any>("");
  
useEffect(() => {
    const getUser = async () => {
      const userData = await getProfile();
      setUser(userData);
      console.log(userData)
    };
    getUser(); 
  }, []);

  useEffect(() => {
    if (user) {
      setDecency(Math.ceil(user.decency / 100));
      setReports(user.reports);
    }
  }, [user]);

  async function HandeChangePassword() {
    await changePassword(currentPassword, newPassword);
    setCurrentPassword("");
    setNewPassword("");
  }

  useEffect(() => {
    if (user) {
      const HandleFriends = async () => {
        const friendsDataValue: Array<string> = await getUserFriends(
          user.username,
          friendsCurrentPage
        );
        setFriendsData(friendsDataValue);
      };
      HandleFriends();

      const HandleFriendsInviteIn = async () => {
        getFriendsRequestIn(friendsInPage)
          .then((res: any) => {
            setFriendsInvite(res);
          }) .catch((error) => {
            console.log(error);
          });
      };
      HandleFriendsInviteIn();
    }
  }, [user]);

  function onCrop(avatar){
    setSelectedPhoto(avatar)
  }

  function onClose(){
    setSelectedPhoto(null)
  }

  async function changeAvatar(){
    if (!selectedPhoto) return
    const fileAvatar = base64toFile(selectedPhoto, 'avatar.png') 
    console.log(fileAvatar)
    await changePhoto(fileAvatar)
  }

  return user ? (
    <div className={`${styles.profile}`}>
      <div className={styles.profile__top}>
        <img
          className={styles.profile__top_bg}
          src="./../../src/assets/profile-bg.jpg"
          alt=""
        />
        <div className={`container ${styles.profile__top_wrapper}`}>
          <div className={styles.profile__top_avatar}>
            <label className={styles.profile__top_change}>
              <AlertDialog>
                <AlertDialogTrigger className={styles.profile__top_trigger}>
                  <ChangePhoto/>        
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>
                    </AlertDialogTitle>
                    <AlertDialogDescription>
                      <Avatar
                        width={462}
                        height={400}
                        labelStyle = {lableStyle}
                        onCrop={onCrop}
                        onClose={onClose}
                        
                      /> 
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>Отмена</AlertDialogCancel>
                    <AlertDialogAction onClick={() => changeAvatar()}>
                      Выберите изображение
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </label>
            <AvatarImg src={userPhoto} size={160} />
          </div>
          <div className={styles.profile__top_text}>
            <p className={`${styles.profile__top_nickname} title`}>
              {user ? <span>{user.username}</span> : null}
            </p>
            <p className={`${styles.profile__top_registratedTime} text`}>
              На сайте с 03.01.2005
            </p>
          </div>
        </div>
      </div>
      <div className={`container ${styles.profile__content} grid grid-cols-6 gap-10`}>
        <div className={`${styles.profile__left} col-span-4 `}>
          <p className="mt-10">История игр</p>
          <div className="flex w-full gap-10">
            <div className={`${styles.profile__decency} mt-10 w-1/2`}>
              <p>Порядочность: {user?.decency} из 1000 </p>
              <Progress value={decency} />
            </div>
            <div className={`${styles.profile__decency} mt-10 w-1/2`}>
              <p>
                На вас было оставлено {reports} жалоб, осталось еще{" "}
                {100 - reports} до временной блокировки{" "}
              </p>
              <Progress value={reports} />
            </div>
          </div>
<div className={`mt-10 ${styles.profile__item}`}>
              <div className={`${styles.profile__row}`}>
                <p>Steam аккаунт</p>
                {user.steamIdExists === true ? (
                  <p>Привязан</p>
                ) : (
                  <a href="https://steamcommunity.com/openid/login?openid.ns=http://specs.openid.net/auth/2.0&openid.mode=checkid_setup&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&openid.identity=http://specs.openid.net/auth/2.0/identifier_select&openid.return_to=https://localhost/steam&openid.realm=https://localhost">
                    Привязать аккаунт
                  </a>
                )}
              </div>
            </div>
            <Separator />
            <div className={`${styles.profile__item}`}>
              <p>Ваш пароль: </p>
              <div className={styles.profile__row}>
                <p>******</p>
                <AlertDialog>
                  <AlertDialogTrigger>Сменить пароль</AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>
                        Вы точно хотите помнять пароль?
                      </AlertDialogTitle>
                      <AlertDialogDescription>
                        <p>Введите текущий пароль</p>
                        <Input
                          value={currentPassword}
                          onChange={(event) => {
                            setCurrentPassword(event.target.value);
                            console.log(event.target.value);
                          }}
                          className="mt-2"
                          type="password"
                        />
                        <p className="mt-2">Введите новый пароль</p>
                        <Input
                          className="mt-2"
                          type="password"
                          value={newPassword}
                          onChange={(event) => {
                            setNewPassword(event.target.value);
                            console.log(event.target.value);
                          }}
                        />
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Отмена</AlertDialogCancel>
                      <AlertDialogAction onClick={() => HandeChangePassword()}>
                        Сменить пароль
                      </AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            </div>
            <Separator />
            <div className={styles.profile__item}>
              <p>Электронная почта: </p>
              <div className={styles.profile__row}>
                <p>{user?.email}</p>
                <AlertDialog>
                  <AlertDialogTrigger>Сменить почту</AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>
                        Are you absolutely sure?
                      </AlertDialogTitle>
                      <AlertDialogDescription>
                        This action cannot be undone. This will permanently
                        delete your account and remove your data from our
                        servers.
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancel</AlertDialogCancel>
                      <AlertDialogAction>Continue</AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            </div>
            <Separator />
            <div className={styles.profile__item}>
              <p>Номер телефона: </p>
              <div className={styles.profile__row}>
                <p>{user?.phoneNumber}</p>
                <AlertDialog>
                  <AlertDialogTrigger>Сменить номер</AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>
                        Are you absolutely sure?
                      </AlertDialogTitle>
                      <AlertDialogDescription>
                        This action cannot be undone. This will permanently
                        delete your account and remove your data from our
                        servers.
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancel</AlertDialogCancel>
                      <AlertDialogAction>Continue</AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            </div>
            <div className="flex flex-col gap-2">
              Выбор темы:
              <div className=" grid grid-cols-4 gap-3">
                <Button
                  onClick={() => {
                    removeBodyClasses();
                    document.querySelector("html")?.classList.add("theme-blue");
                  }}
                >
                  Синяя тема
                </Button>
                <Button
                  onClick={() => {
                    removeBodyClasses();
                    document.querySelector("html")?.classList.add("theme-red");
                  }}
                >
                  Красная тема
                </Button>
                <Button
                  onClick={() => {
                    removeBodyClasses();
                    document
                      .querySelector("html")
                      ?.classList.add("theme-orange");
                  }}
                >
                  Оранжевая тема
                </Button>
                <Button
                  onClick={() => {
                    removeBodyClasses();
                    document.querySelector("html")?.classList.add("theme-zink");
                  }}
                >
                  Серая тема
                </Button>
                <Button
                  onClick={() => {
                    removeBodyClasses();
                    document
                      .querySelector("html")
                      ?.classList.add("theme-violet");
                  }}
                >
                  Фиолетовая тема
                </Button>
              </div>
            </div>
        </div>
        <div className={styles.profile__right}>
                         <div className="">
              {friendsInvite
                ? friendsInvite.map((request: any) => (
                    <Friend
                      username={request.username}
                      type="in"
                      avatar={request.photo}
                    />
                  ))
                : null}
              <p className={`mt-10 ${styles.friends__title}`}>Список друзей:</p>
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
                <p
                  className={styles.friends__text}
                >{`У вас пока что нет ни одного друга, но не стоит расстраиваться...`}</p>
              )}
            </div>
        </div>
      </div>
    </div>
  ) : null;
}
