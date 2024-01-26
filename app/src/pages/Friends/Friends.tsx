import styles from './Friends.module.sass';
import { useEffect, useState } from 'react';
import { useAppDispatch } from '@/hooks/useAppDispatch';
import { useAppSelector } from '@/hooks/useAppSelector';
import { useDebounce } from '@/hooks/useDebounce';
import Friend from '../../components/Friends/Friend/Friend';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  setFriendsCurrent,
  setFriendsIn,
  setFriendsOut,
} from '@/store/reducers/friendsSlice';
import Preloader from '@/components/Preloader';
import Pagination from '@/components/Pagination/Pagination';
import userService from '@/service/user.service';
import friendsService from '@/service/friends.service';

export default function Friends() {
  const username = useAppSelector((state) => state.userReducer.username);

  const [isLoading, setIsLoading] = useState(false);

  const isAuth = useAppSelector((state) => state.authReducer.data);
  const isFriendsActive = useAppSelector((state) => state.menusReduce.friends);

  const [searchedUsers, setSearchedUsers] = useState<Array<string>>([]);
  const [queryNickname, setQueryNickname] = useState('');

  const [friendsInPage, setFriendsInPage] = useState<number>(1);
  const [friendsOutPage, setFriendsOutPage] = useState<number>(1);
  const [friendsCurrentPage, setFriendsCurrentPage] = useState<number>(1);

  const friendsIn = useAppSelector((state) => state.friendsSlice.in);
  const friendsOut = useAppSelector((state) => state.friendsSlice.out);
  const friendsCurrent = useAppSelector((state) => state.friendsSlice.current);

  const [friendsInPageNext, setFriendsInPageNext] = useState<boolean>(false);
  const [friendsOutPageNext, setFriendsOutPageNext] = useState<boolean>(false);
  const [friendsCurrentPageNext, setFriendsCurrentPageNext] =
    useState<boolean>(false);

  const dispath = useAppDispatch();

  const debouncedSearchUsers = useDebounce(queryNickname);

  useEffect(() => {
    if (queryNickname.length < 2) return;
    setIsLoading(true);
    async function getSearchedUsers() {
      if (queryNickname.length > 2) {
        async function getRequest() {
          await friendsService.searchUsers(debouncedSearchUsers, 1).then((res) => {
            setSearchedUsers(res);
          });
        }
        getRequest();
      } else {
        setSearchedUsers([]);
      }
    }
    getSearchedUsers();
    setIsLoading(false);
  }, [debouncedSearchUsers]);

  useEffect(() => {
    const HandleFriends = async () => {
      await friendsService
        .getUserFriends(username, friendsCurrentPage)
        .then((res) => {
          if (res.length == 20) {
            friendsService
              .getUserFriends(username, friendsCurrentPage + 1)
              .then((res) => {
                if (res.length > 0) {
                  setFriendsCurrentPageNext(true);
                } else {
                  setFriendsCurrentPageNext(false);
                }
              });
          } else {
            setFriendsCurrentPageNext(false);
          }
          dispath(setFriendsCurrent(res));
        });
    };
    HandleFriends();
  }, [friendsCurrentPage]);

  useEffect(() => {
    const HandleFriendsInviteIn = async () => {
      friendsService
        .getRequestInByPage(friendsInPage)
        .then((res) => {
          if (res.length == 20) {
            userService.getRequestInByPage(friendsInPage + 1).then((res) => {
              if (res.length > 0) {
                setFriendsInPageNext(true);
              } else setFriendsInPageNext(false);
            });
          } else setFriendsInPageNext(false);
          dispath(setFriendsIn(res));
        })
        .catch((error) => {
          console.log(error);
        });
    };
    HandleFriendsInviteIn();
  }, [friendsInPage]);

  useEffect(() => {
    const HandleFriendsInviteOut = async () => {
      friendsService
        .getRequestOutByPage(friendsOutPage)
        .then((res) => {
          if (res.length == 20) {
            friendsService
              .getRequestOutByPage(friendsOutPage + 1)
              .then((res) => {
                if (res.length > 0) {
                  setFriendsOutPageNext(true);
                } else setFriendsOutPageNext(false);
              });
          } else setFriendsOutPageNext(false);
          dispath(setFriendsOut(res));
        })
        .catch((error) => {
          console.log(error);
        });
    };
    HandleFriendsInviteOut();
  }, [friendsOutPage]);

  return isAuth ? (
    <div
      className={`${styles.friends} ${
        isFriendsActive ? styles.friends_active : null
      }`}
    >
      <Tabs defaultValue="friends" className="">
        <TabsList>
          <TabsTrigger value="friends">
            Друзья ({' '}
            {friendsCurrent.length == 20 || friendsCurrentPage > 1
              ? '20+'
              : friendsCurrent.length}{' '}
            )
          </TabsTrigger>
          <TabsTrigger value="friendsIn">
            Заявки в друзья ({' '}
            {friendsIn.length == 20 || friendsInPage > 1
              ? '20+'
              : friendsIn.length}{' '}
            )
          </TabsTrigger>
          <TabsTrigger value="friendsOut">
            Отправленные заявки ({' '}
            {friendsOut.length == 20 || friendsOutPage > 1
              ? '20+'
              : friendsOut.length}{' '}
            )
          </TabsTrigger>
          <TabsTrigger value="search">Поиск</TabsTrigger>
        </TabsList>
        <TabsContent value="friends">
          <div className={styles.wrapper}>
            <div className={styles.list}>
              {friendsCurrent.length == 0 ? (
                <p>
                  У вас пока что нет ни одного друга, но не стоит
                  расстраиваться...
                </p>
              ) : (
                friendsCurrent.map((friend) => (
                  <Friend
                    key={friend.username}
                    username={friend.username}
                    type="current"
                    avatar={friend.photo}
                  />
                ))
              )}
            </div>
            <Pagination
              page={friendsCurrentPage}
              next={friendsCurrentPageNext}
              setPage={setFriendsCurrentPage}
            />
          </div>
        </TabsContent>
        <TabsContent value="friendsIn">
          <div className={styles.wrapper}>
            <div className={styles.list}>
              {friendsIn
                ? friendsIn.map((request) => (
                    <Friend
                      key={request.username}
                      username={request.username}
                      type="in"
                      avatar={request.photo}
                    />
                  ))
                : null}
            </div>
            <Pagination
              page={friendsInPage}
              next={friendsInPageNext}
              setPage={setFriendsInPage}
            />
          </div>
        </TabsContent>
        <TabsContent value="friendsOut">
          <div className={styles.wrapper}>
            <div className={styles.list}>
              {friendsOut
                ? friendsOut.map((request) => (
                    <Friend
                      key={request.username}
                      username={request.username}
                      type="out"
                      avatar={request.photo}
                    />
                  ))
                : null}
            </div>
            <Pagination
              page={friendsOutPage}
              next={friendsOutPageNext}
              setPage={setFriendsOutPage}
            />
          </div>
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
                friendsService.addfriend(queryNickname);
              }}
            >
              Отправить заявку
            </Button>
          </div>
          <div className={`${styles.list}`}>
            {isLoading ? (
              <Preloader />
            ) : (
              <>
                {queryNickname.length > 2 && searchedUsers.length == 0 && (
                  <p className="text-center">
                    Пользователей с таким именем не найдено
                  </p>
                )}
                {searchedUsers.map((user: any) => (
                  <Friend
                    username={user.username}
                    type="search"
                    avatar={user.photo}
                  />
                ))}
              </>
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  ) : null;
}
