import React, { useEffect, useState } from "react";
import styles from "./Friends.module.sass";
import { useSelector } from "react-redux";
import getUserFriends from "../../api/getUserFriends";
import sendFriendRequest from "../../api/sendFriendRequest";
import getUsersByValue from "../../api/getUsersByValue";
import { RootState } from "../../store/store";
import IUsername from "../../interfaces/IUsername";
import { useAppSelector, useDebounce } from "../../hooks";
import getFriendsRequestIn from "../../api/getFriendsRequestIn";
import { error } from "console";
import getFriendsRequestOut from "../../api/getFriendsRequestOut";
import Friend from "../../components/Friends/Friend/Friend";
import { Navigate } from "react-router-dom";

export default function Friends() {
  const username: string = useSelector(
    (state: RootState) => state.userReducer.username
  );
  const [searchedUsers, setSearchedUsers] = useState<Array<string>>([]);
  const [friendsData, setFriendsData] = useState<any>([]);
  const [queryNickname, setQueryNickname] = useState("");
  const [friendsInvite, setFriendsInvite] = useState([]);
  const [friendsRequest, setFriendsRequest] = useState<any>([]);

  const isAuth = useAppSelector((state) => state.authReducer.data);

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
        .then((res) => {
          console.log(res);
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
    <div className={`container ${styles.friends}`}>
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
      <div className={`${styles.list}`}>
        <p className="title">Отправленные заявки в друзья</p>
        {friendsRequest
          ? friendsRequest.map((request: any) => (
              <Friend
                username={request.username}
                type="out"
                avatar={request.photo}
              />
            ))
          : null}
        <p className="title">Список друзей:</p>
        {friendsData ? (
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
          <p className="text">{`У вас нет друзей :(`}</p>
        )}
      </div>
    </div>
  ) : (
    <Navigate to="/login" />
  );
}
