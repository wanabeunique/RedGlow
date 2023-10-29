import { useEffect, useState } from "react";
import styles from "./Friends.module.sass";
import getUserFriends from "../../api/getUserFriends";
import sendFriendRequest from "../../api/sendFriendRequest";
import getUsersByValue from "../../api/getUsersByValue";
import { useAppDispatch, useAppSelector, useDebounce } from "../../hooks";
import getFriendsRequestIn from "../../api/getFriendsRequestIn";
import getFriendsRequestOut from "../../api/getFriendsRequestOut";
import Friend from "../../components/Friends/Friend/Friend";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { setFriendsCurrent, setFriendsIn, setFriendsOut } from "@/store/reducers/friendsSlice";

export default function Friends() {
  const username: string = useAppSelector(
    (state) => state.userReducer.username
  );
  const [searchedUsers, setSearchedUsers] = useState<Array<string>>([]);
  const [queryNickname, setQueryNickname] = useState("");

  const isAuth = useAppSelector((state) => state.authReducer.data);
  const isFriendsActive = useAppSelector((state) => state.menusReduce.friends);
  const friendsIn = useAppSelector((state) => state.friendsSlice.in)
  const friendsOut = useAppSelector((state) => state.friendsSlice.out)
  const friendsCurrent = useAppSelector((state) => state.friendsSlice.current)
  const dispath = useAppDispatch()

  const debouncedSearchUsers = useDebounce(queryNickname);

  useEffect(() => {
    async function getSearchedUsers() {
      if (queryNickname.length > 2) {
        async function getRequest() {
          await getUsersByValue(debouncedSearchUsers, 1).then((res) => {
            setSearchedUsers(res);
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
        .then((res) => dispath(setFriendsCurrent(res)));
    };
    HandleFriends();

    const HandleFriendsInviteIn = async () => {
      getFriendsRequestIn()
        .then((res: any) => {
          dispath(setFriendsIn(res))
        })
        .catch((error) => {
          console.log(error);
        });
    };
    HandleFriendsInviteIn();

    const HandleFriendsInviteOut = async () => {
      getFriendsRequestOut()
        .then((res: any) => {
          dispath(setFriendsOut(res))
        })
        .catch((error) => {
          console.log(error);
        });
    };
    HandleFriendsInviteOut();
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
            Друзья ( {friendsCurrent.length} )
          </TabsTrigger>
          <TabsTrigger value="friendsIn">
            Заявки в друзья ( {friendsIn.length} )
          </TabsTrigger>
          <TabsTrigger value="friendsOut">
            Отправленные заявки ( {friendsOut.length} )
          </TabsTrigger>
          <TabsTrigger value="search">Поиск</TabsTrigger>
        </TabsList>
        <TabsContent value="friends">
          {friendsCurrent.length == 0 ? (
            <p>У вас пока что нет ни одного друга, но не стоит расстраиваться...</p>
          )
          : friendsCurrent.map(
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
          {friendsIn
            ? friendsIn.map((request: any) => (
                <Friend
                  username={request.username}
                  type="in"
                  avatar={request.photo}
                />
              ))
            : null}
        </TabsContent>
        <TabsContent value="friendsOut">
          {friendsOut
            ? friendsOut.map((request: any) => (
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
