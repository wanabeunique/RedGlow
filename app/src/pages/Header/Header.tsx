import styles from "./Header.module.sass";
import Avatar from "@/components/SVG/Avatar";
import { Link, NavLink } from "react-router-dom";
import setLogout from "../../api/setLogout";
import { useAppDispatch, useAppSelector } from "../../hooks";
import {
  setFriendsMenuActive,
  setProfileMenuActive,
} from "../../store/reducers/isMenusActiveSlice";
import { ModeToggle } from "@/components/mode-toggle";

export default function Header() {
  const dispatch = useAppDispatch();
  const isAuth = useAppSelector((state) => state.authReducer.data);
  const nickname = useAppSelector((state) => state.userReducer.username);
  const photo = useAppSelector((state) => state.userReducer.photo)

  const isFriendsActive = useAppSelector((state) => state.menusReduce.friends);

  function HandleFriends() {
    dispatch(setFriendsMenuActive(!isFriendsActive));
    dispatch(setProfileMenuActive(false));
  }

  return (
    <header className={` ${styles.header} `}>
      <div className={`container ${styles.header__container}`}>
        <div className={`${styles.header__left}`}>
          <Link to={"/"} className={styles.header__logo}>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="27"
              height="37"
              viewBox="0 0 27 37"
              fill="none"
            >
              <path
                d="M25.5939 13.4688H17.0275L26.4791 21.8672C26.6836 22.0475 26.8284 22.2858 26.8943 22.5503C26.9601 22.8149 26.944 23.0932 26.8479 23.3484C26.7519 23.6036 26.5805 23.8235 26.3565 23.9789C26.1325 24.1344 25.8666 24.218 25.5939 24.2188H14.8439V34.9688C14.8441 35.2347 14.7654 35.4947 14.6178 35.7159C14.4702 35.937 14.2602 36.1094 14.0146 36.2112C13.7689 36.313 13.4985 36.3396 13.2377 36.2877C12.9769 36.2357 12.7374 36.1076 12.5495 35.9195L0.455728 23.8257C0.330982 23.7008 0.232063 23.5526 0.164623 23.3895C0.0971827 23.2263 0.0625427 23.0515 0.0626815 22.875V12.125C0.0626815 11.7686 0.204255 11.4268 0.456257 11.1748C0.708259 10.9228 1.05005 10.7813 1.40643 10.7813H9.97284L0.514517 2.38282C0.309609 2.20211 0.164654 1.96323 0.0989755 1.69803C0.0332975 1.43283 0.0500179 1.15391 0.146907 0.898461C0.243797 0.643008 0.416252 0.423158 0.641281 0.268221C0.866311 0.113283 1.13322 0.0306211 1.40643 0.0312536H25.5939C25.9503 0.0312536 26.2921 0.172827 26.5441 0.424829C26.7961 0.676831 26.9377 1.01862 26.9377 1.375V12.125C26.9377 12.4814 26.7961 12.8232 26.5441 13.0752C26.2921 13.3272 25.9503 13.4688 25.5939 13.4688Z"
                fill="#B32428"
              />
            </svg>
          </Link>
          <NavLink to="/Generate" className={`${styles.menu__title} ${styles.menu__link_white}`}>
            Генерация наций
          </NavLink>
          <NavLink to="/headbook" className={`${styles.menu__title} ${styles.menu__link_white}`}>
            Справочник
          </NavLink>
          {isAuth ? (
            <>
              <li className={styles.header__item}>
                <NavLink to="/Play">
                  Играть
                </NavLink>
              </li>
              <li
                className={styles.header__item}
                onClick={() => {
                  dispatch<any>(setLogout());
                }}
              >
                <NavLink
                  to="/headbook"
                  className={`${styles.header__link}`}
                >
                  Выйти
                </NavLink>
              </li>
            </>
          ) : (
            <></>
          )}
        </div>
        <div className={styles.header__right}>
          <ModeToggle />
          <ul className={styles.header__items}>
            {isAuth ? (
              <>
                <li className={styles.header__item}>
                  <svg
                    className={`${styles.header__friends} ${
                      isFriendsActive
                        ? `${styles.header__friends_active}`
                        : null
                    }`}
                    onClick={() => {
                      HandleFriends();
                    }}
                    width="25px"
                    height="25px"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      opacity="0.1"
                      d="M13 9.5C13 11.433 11.433 13 9.5 13C7.567 13 6 11.433 6 9.5C6 7.567 7.567 6 9.5 6C11.433 6 13 7.567 13 9.5Z"
                      fill="#323232"
                    />
                    <path
                      d="M15.6309 7.15517C15.9015 7.05482 16.1943 7 16.4999 7C17.8806 7 18.9999 8.11929 18.9999 9.5C18.9999 10.8807 17.8806 12 16.4999 12C16.1943 12 15.9015 11.9452 15.6309 11.8448"
                      stroke="#323232"
                      stroke-width="2"
                      stroke-linecap="round"
                    />
                    <path
                      d="M3 19C3.69137 16.6928 5.46998 16 9.5 16C13.53 16 15.3086 16.6928 16 19"
                      stroke="#323232"
                      stroke-width="2"
                      stroke-linecap="round"
                    />
                    <path
                      d="M17 15C19.403 15.095 20.5292 15.6383 21 17"
                      stroke="#323232"
                      stroke-width="2"
                      stroke-linecap="round"
                    />
                    <path
                      d="M13 9.5C13 11.433 11.433 13 9.5 13C7.567 13 6 11.433 6 9.5C6 7.567 7.567 6 9.5 6C11.433 6 13 7.567 13 9.5Z"
                      stroke="#323232"
                      stroke-width="2"
                    />
                  </svg>
                </li>
                <li className={`${styles.header__item}`}>
                  <NavLink
                    to={`/profile/${nickname}`}
                    className={`text ${styles.header__link} ${styles.header__profile}`}
                  >
                    {photo ? (<img className={styles.header__avatar} src={`${photo}`} />) : <Avatar /> }
                    
                    <div className={styles.header__profile_fields}>
                      <p className={`text ${styles.header__profile_nick}`}>
                        {nickname}
                      </p>
                      <p className={styles.header__profile_points}>R 0</p>
                    </div>
                  </NavLink>
                </li>
              </>
            ) : (
              <>
                <li className={styles.header__item}>
                  <NavLink
                    to="/Login"
                    className={`text ${styles.header__link}`}
                  >
                    Войти
                  </NavLink>
                </li>
                <li className={styles.header__item}>
                  <NavLink
                    to="/Registration"
                    className={`text ${styles.header__link}`}
                  >
                    Регистрация
                  </NavLink>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </header>
  );
}
