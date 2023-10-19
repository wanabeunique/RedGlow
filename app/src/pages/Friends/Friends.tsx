import { useEffect, useState } from "react";
import styles from "./Friends.module.sass";
import getUserFriends from "../../api/getUserFriends";
import sendFriendRequest from "../../api/sendFriendRequest";
import getUsersByValue from "../../api/getUsersByValue";
import { useAppSelector, useDebounce } from "../../hooks";
import getFriendsRequestIn from "../../api/getFriendsRequestIn";
import getFriendsRequestOut from "../../api/getFriendsRequestOut";
import Friend from "../../components/Friends/Friend/Friend";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function Friends() {
  const username: string = useAppSelector(
    (state) => state.userReducer.username
  );
  const [searchedUsers, setSearchedUsers] = useState<Array<string>>([]);
  const [friendsData, setFriendsData] = useState<any>([]);
  const [queryNickname, setQueryNickname] = useState("");
  const [friendsInvite, setFriendsInvite] = useState([]);
  const [friendsRequest, setFriendsRequest] = useState<any>([]);

  const isAuth = useAppSelector((state) => state.authReducer.data);
  const isFriendsActive = useAppSelector((state) => state.menusReduce.friends);

  const debouncedSearchUsers = useDebounce(queryNickname);

  useEffect(() => {
    async function getSearchedUsers() {
      if (queryNickname.length > 2) {
        async function getRequest() {
          await getUsersByValue(debouncedSearchUsers, 1).then((res) => {
            setSearchedUsers(res);
            console.log(res);
          });
        }
        getRequest();
      } else {
        setSearchedUsers([]);
      }
    }
    getSearchedUsers();
  }, [debouncedSearchUsers]);

  useEffect(() => {
    const HandleFriends = async () => {
      await getUserFriends(username)
        .then((res) => setFriendsData(res));
    };
    HandleFriends();

    const HandleFriendsInviteIn = async () => {
      getFriendsRequestIn()
        .then((res: any) => {
          setFriendsInvite(res);
        })
        .catch((error) => {
          console.log("IN");
          console.log(error);
        });
    };
    HandleFriendsInviteIn();

    const HandleFriendsInviteOut = async () => {
      getFriendsRequestOut()
        .then((res: any) => {
          setFriendsRequest(res);
        })
        .catch((error) => {
          console.log("OUT");
          console.log(error);
        });
    };
    HandleFriendsInviteOut();

    console.log(friendsData, typeof(friendsData));
  }, []);

  return isAuth ? (
    <div
      className={`${styles.friends} ${
        isFriendsActive ? styles.friends_active : null
      }`}
    >
      <Tabs defaultValue="friends" className="">
        <TabsList>
          <TabsTrigger value="friends">
            Друзья ( {friendsData.length} )
          </TabsTrigger>
          <TabsTrigger value="friendsIn">
            Заявки в друзья ( {friendsInvite.length} )
          </TabsTrigger>
          <TabsTrigger value="friendsOut">
            Отправленные заявки ( {friendsRequest.length} )
          </TabsTrigger>
          <TabsTrigger value="search">Поиск</TabsTrigger>
        </TabsList>
        <TabsContent value="friends">
          {friendsData.length == 0 ? (
            <p>У вас пока что нет ни одного друга, но не стоит расстраиваться...</p>
          )
          : friendsData.map(
            ((friend: any) => (
              <Friend
                username={friend.username}
                type="current"
                avatar={friend.photo}
              /> 
            ))
          )
          }
        </TabsContent>
        <TabsContent value="friendsIn">
          {friendsInvite
            ? friendsInvite.map((request: any) => (
                <Friend
                  username={request.username}
                  type="in"
                  avatar={request.photo}
                />
              ))
            : null}
        </TabsContent>
        <TabsContent value="friendsOut">
          {friendsRequest
            ? friendsRequest.map((request: any) => (
                <Friend
                  username={request.username}
                  type="out"
                  avatar={request.photo}
                />
              ))
            : null}
        </TabsContent>
        <TabsContent value="search">
          <div className={styles.search}>
            <Input
              onChange={(event) => {
                setQueryNickname(event.target.value);
                setSearchedUsers;
              }}
              value={queryNickname}
              type="text"
              placeholder="Введите имя друга..."
            />
            <Button
              onClick={() => {
                sendFriendRequest(queryNickname);
              }}
            >
              Отправить заявку
            </Button>
          </div>
          <div className={`${styles.list_search}`}>
            <>
              {queryNickname.length > 2 && searchedUsers.length == 0 && (
                <p className='text-center'>Пользователей с таким именем не найдено</p>
              )}
              {searchedUsers.map((user: any) => (
                <Friend
                  username={user.username}
                  type="search"
                  avatar={user.photo}
                />
              ))}
            </>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  ) : null;
}
