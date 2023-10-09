import { useEffect, useState } from "react";
import styles from "./Friends.module.sass";
import getUserFriends from "../../api/getUserFriends";
import sendFriendRequest from "../../api/sendFriendRequest";
import getUsersByValue from "../../api/getUsersByValue";
import { useAppSelector, useDebounce } from "../../hooks";
import getFriendsRequestIn from "../../api/getFriendsRequestIn";
import getFriendsRequestOut from "../../api/getFriendsRequestOut";
import Friend from "../../components/Friends/Friend/Friend";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";

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
          await getUsersByValue(debouncedSearchUsers).then((res) => {
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
      const friendsDataValue: Array<string> = await getUserFriends(username);
      setFriendsData(friendsDataValue);
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

    console.log(friendsData);
  }, []);

  return isAuth ? (
    <div
      className={`container ${styles.friends} ${
        isFriendsActive ? styles.friends_active : null
      }`}
    >
      <Tabs className={styles.friends__tabs}>
        <TabList className={styles.friends__top}>
          <Tab className={styles.friends__tab}>
            Друзья ( {friendsData.length} )
          </Tab>
          <Tab className={styles.friends__tab}>
            Заявки в дурзья ( {friendsInvite.length} )
          </Tab>
          <Tab className={styles.friends__tab}>
            Отправленные заявки ( {friendsRequest.length} )
          </Tab>
          <Tab className={styles.friends__tab}>Поиск</Tab>
        </TabList>
        <TabPanel className={styles.friends__content}>
          <p className={styles.friends__title}>Список друзей:</p>
          {friendsData.lenght > 0 ? (
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
            >{`У вас пока что нет ни одного друга, но не стоит расстраиваться...`}</p>
          )}
        </TabPanel>
        <TabPanel>
          {friendsInvite
            ? friendsInvite.map((request: any) => (
                <Friend
                  username={request.username}
                  type="in"
                  avatar={request.photo}
                />
              ))
            : null}
        </TabPanel>
        <TabPanel className={styles.friends__content}>
          <p className={styles.friends__title}>Отправленные заявки в друзья</p>
          {friendsRequest
            ? friendsRequest.map((request: any) => (
                <Friend
                  username={request.username}
                  type="out"
                  avatar={request.photo}
                />
              ))
            : null}
        </TabPanel>
        <TabPanel>
          <div className={styles.search}>
            <input
              onChange={(event) => {
                setQueryNickname(event.target.value);
                setSearchedUsers;
              }}
              value={queryNickname}
              className={`${styles.search__input} input`}
              type="text"
              placeholder="Введите имя друга..."
            />
            <button
              onClick={() => {
                sendFriendRequest(queryNickname);
              }}
              className={`${styles.search__button} button`}
            >
              Отправить заявку
            </button>
          </div>
          <div className={`${styles.list_search}`}>
            <>
              {searchedUsers.map((user: any) => (
                <Friend
                  username={user.nickname}
                  type="search"
                  avatar={user.photo}
                />
              ))}
            </>
          </div>
        </TabPanel>
      </Tabs>
    </div>
  ) : null;
}
