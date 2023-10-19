import getUserProfile from "@/api/getUserProfile";
import styles from "./Proflie.module.sass";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Avatar } from "antd";
import { Progress } from "@/components/ui/progress";
import IProfile from "@/interfaces/IProfile";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import getUserFriends from "@/api/getUserFriends";
import Friend from "@/components/Friends/Friend/Friend";

interface IUserProfile{
  username: string
}

export default function UserProfile({username}: IUserProfile) {
  console.log(username)
  const navigate = useNavigate();
  const [friendsData, setFriendsData] = useState<any>([]);
  const [user, setUser] = useState<IProfile>();
  useEffect(() => {
    async function fetchUser() {
      const user = await getUserProfile(username);
      if (!user) {
        return navigate("/");
      }
      console.log(user, 'user')
      const friends = await getUserFriends(user?.username);
      setFriendsData(friends);
      setUser(user);
    }
    fetchUser();
  }, []);
  return (
    <div className={`${styles.profile}`}>
      <div className={styles.profile__top}>
        <img
          className={styles.profile__top_bg}
          src="./../../src/assets/profile-bg.jpg"
          alt=""
        />
        <div className={`container ${styles.profile__top_wrapper}`}>
          <div className={styles.profile__top_avatar}>
            <Avatar size={160} />
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
      <div className={`container ${styles.profile__content}`}>
        <Tabs defaultValue="review" className="">
          <TabsList>
            <TabsTrigger value="review">Обзор</TabsTrigger>
            <TabsTrigger value="history">История</TabsTrigger>
            <TabsTrigger value="friends">Друзья</TabsTrigger>
          </TabsList>
          <TabsContent value="review">
            <div className={`${styles.profile__decency} mt-10`}>
              <p>Порядочность: {user?.decency} из 1000 </p>
              <Progress value={user?.decency} />
            </div>
            <div className={`${styles.profile__decency} mt-10`}>
              <p>
                На {user?.username} было оставлено {user?.reports} жалоб
              </p>
              <Progress value={user?.reports} />
            </div>
          </TabsContent>
          <TabsContent value="history">
            <p className="mt-10">История игр</p>
          </TabsContent>
          <TabsContent value="friends">
            <div>
              <p className={`mt-10 ${styles.friends__title}`}>Список друзей:</p>
              {friendsData.length > 0 ? (
                <div className={styles.friends__items}>
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
                >{`У ${user?.username} пока что нет ни одного друга`}</p>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
