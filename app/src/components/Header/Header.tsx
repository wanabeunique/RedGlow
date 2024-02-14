import styles from './Header.module.sass';
import Avatar from '@/components/SVG/Avatar';
import { Link, NavLink } from 'react-router-dom';
import { useAppDispatch } from '@/hooks/useAppDispatch';
import { useAppSelector } from '@/hooks/useAppSelector';
import {
  setFriendsMenuActive,
  setProfileMenuActive,
} from '@/store/reducers/isMenusActiveSlice';
import { ModeToggle } from '@/components/ui/mode-toggle';
import { ReactSVG } from 'react-svg';
import authService from '@/service/auth.service';

export default function Header() {
  const dispatch = useAppDispatch();

  const isAuth = useAppSelector((state) => state.authReducer.data);
  const nickname = useAppSelector((state) => state.userReducer.username);
  const photo = useAppSelector((state) => state.userReducer.photo);

  const isFriendsActive = useAppSelector((state) => state.menusReduce.friends);

  function HandleFriends() {
    dispatch(setFriendsMenuActive(!isFriendsActive));
    dispatch(setProfileMenuActive(false));
  }

  return (
    <header className={` ${styles.header} `}>
      <div className={`container ${styles.header__container}`}>
        <div className={`${styles.header__left}`}>
          <Link to={'/'} className={styles.header__logo}>
            <ReactSVG src="imgs/logo.svg" />
          </Link>
          {isAuth ? (
            <>
              <li className={styles.header__item}>
                <NavLink to="/Play">Играть</NavLink>
              </li>
              <li
                className={styles.header__item}
                onClick={() => {
                  authService.logout();
                }}
              >
                <NavLink to="/headbook" className={`${styles.header__link}`}>
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
                  <div
                    className={`${styles.header__friends} ${
                      isFriendsActive
                        ? `${styles.header__friends_active}`
                        : null
                    }`}
                    onClick={() => {
                      HandleFriends();
                    }}
                  >
                    <ReactSVG src="/imgs/friends.svg" />
                  </div>
                </li>
                <li className={`${styles.header__item}`}>
                  <NavLink
                    to={`/profile/${nickname}`}
                    className={`text ${styles.header__link} ${styles.header__profile}`}
                  >
                    {photo ? (
                      <img className={styles.header__avatar} src={`${photo}`} />
                    ) : (
                      <Avatar />
                    )}

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
                    to="/login"
                    className={`text ${styles.header__link}`}
                  >
                    Войти
                  </NavLink>
                </li>
                <li className={styles.header__item}>
                  <NavLink
                    to="/registration"
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
