import React from 'react'
import styles from './Header.module.sass'
import { Link, NavLink } from 'react-router-dom'
import { Avatar } from 'antd'
import { useSelector } from 'react-redux'
import logout from '../../api/logout'
import { useDispatch } from "react-redux";

export default function Header() {
  const dispatch = useDispatch()
  const isAuth = useSelector((state) => state.authReducer.data)
  const nickname = useSelector((state) => state.userReducer.username)
  return (
    <header className={styles.header}>
      <div className={`container ${styles.header__container}`}>
        <div className={`${styles.header__left}`}>
          <Link to={'/'} className={styles.header__logo}>
            <svg xmlns="http://www.w3.org/2000/svg" width="27" height="37" viewBox="0 0 27 37" fill="none">
              <path d="M25.5939 13.4688H17.0275L26.4791 21.8672C26.6836 22.0475 26.8284 22.2858 26.8943 22.5503C26.9601 22.8149 26.944 23.0932 26.8479 23.3484C26.7519 23.6036 26.5805 23.8235 26.3565 23.9789C26.1325 24.1344 25.8666 24.218 25.5939 24.2188H14.8439V34.9688C14.8441 35.2347 14.7654 35.4947 14.6178 35.7159C14.4702 35.937 14.2602 36.1094 14.0146 36.2112C13.7689 36.313 13.4985 36.3396 13.2377 36.2877C12.9769 36.2357 12.7374 36.1076 12.5495 35.9195L0.455728 23.8257C0.330982 23.7008 0.232063 23.5526 0.164623 23.3895C0.0971827 23.2263 0.0625427 23.0515 0.0626815 22.875V12.125C0.0626815 11.7686 0.204255 11.4268 0.456257 11.1748C0.708259 10.9228 1.05005 10.7813 1.40643 10.7813H9.97284L0.514517 2.38282C0.309609 2.20211 0.164654 1.96323 0.0989755 1.69803C0.0332975 1.43283 0.0500179 1.15391 0.146907 0.898461C0.243797 0.643008 0.416252 0.423158 0.641281 0.268221C0.866311 0.113283 1.13322 0.0306211 1.40643 0.0312536H25.5939C25.9503 0.0312536 26.2921 0.172827 26.5441 0.424829C26.7961 0.676831 26.9377 1.01862 26.9377 1.375V12.125C26.9377 12.4814 26.7961 12.8232 26.5441 13.0752C26.2921 13.3272 25.9503 13.4688 25.5939 13.4688Z" fill="#B32428"/>
            </svg>
          </Link>
          <li className={styles.header__item}><NavLink to='/' className={`text ${styles.header__link}`}>Главная</NavLink></li>
          <li className={styles.header__item}><NavLink to='/Generate' className={`text ${styles.header__link}`}>Генерация наций</NavLink></li>
          <li className={styles.header__item}><NavLink to='/headbook' className={`text ${styles.header__link}`}>Справочник</NavLink></li>
          {isAuth ?
          (
            <>
              <li className={styles.header__item}><NavLink to='/Friends' className={`text ${styles.header__link}`}>Друзья</NavLink></li>
              <li className={styles.header__item}><NavLink to='/Play' className={`text ${styles.header__link}`}>Играть</NavLink></li>
              <li className={styles.header__item} onClick={() => {logout(dispatch)}}><NavLink to='/headbook' className={`text ${styles.header__link}`}>Выйти</NavLink></li>
            </>
          )
          :  (
            <>
            </>
          )     
          }
        </div>
        <div className="header__right">
        <ul className={styles.header__items}>
          {isAuth ?
          (
            <>
              <li className={`${styles.header__item}`}>
                <NavLink to='/Profile' className={`text ${styles.header__link} ${styles.header__profile}`}>
                  {/* <Avatar /> */}
                  <svg xmlns="http://www.w3.org/2000/svg" width="43" height="43" viewBox="0 0 43 43" fill="none">
                    <circle cx="21.5" cy="21.5" r="20.5" stroke="white" stroke-width="2"/>
                    <path opacity="0.16" d="M11.4667 28.4235C11.4667 27.0714 12.0038 25.7746 12.9599 24.8186C13.916 23.8625 15.2127 23.3254 16.5648 23.3254H26.761C28.1131 23.3254 29.4098 23.8625 30.3659 24.8186C31.322 25.7746 31.8591 27.0714 31.8591 28.4235C31.8591 29.0995 31.5906 29.7479 31.1125 30.2259C30.6345 30.704 29.9861 30.9725 29.3101 30.9725H14.0157C13.3397 30.9725 12.6913 30.704 12.2133 30.2259C11.7352 29.7479 11.4667 29.0995 11.4667 28.4235Z" fill="white"/>
                    <path d="M11.4667 28.4235C11.4667 27.0714 12.0038 25.7746 12.9599 24.8186C13.916 23.8625 15.2127 23.3254 16.5648 23.3254H26.761C28.1131 23.3254 29.4098 23.8625 30.3659 24.8186C31.322 25.7746 31.8591 27.0714 31.8591 28.4235C31.8591 29.0995 31.5906 29.7479 31.1125 30.2259C30.6345 30.704 29.9861 30.9725 29.3101 30.9725H14.0157C13.3397 30.9725 12.6913 30.704 12.2133 30.2259C11.7352 29.7479 11.4667 29.0995 11.4667 28.4235Z" stroke="white" stroke-width="2" stroke-linejoin="round"/>
                    <path d="M21.2196 20.333C23.668 20.333 25.6528 18.3482 25.6528 15.8998C25.6528 13.4515 23.668 11.4667 21.2196 11.4667C18.7713 11.4667 16.7865 13.4515 16.7865 15.8998C16.7865 18.3482 18.7713 20.333 21.2196 20.333Z" stroke="white" stroke-width="2"/>
                  </svg>
                  <div className={styles.header__profile_fields}>
                    <p className={`text ${styles.header__profile_nick}`}>{nickname}</p>
                    <p className={styles.header__profile_points}>R 0</p>
                  </div>
                </NavLink>
              </li>
            </>
          )
          :  (
            <>
              <li className={styles.header__item}><NavLink to='/Login' className={`text ${styles.header__link}`}>Войти</NavLink></li>
              <li className={styles.header__item}><NavLink to='/Registration' className={`text ${styles.header__link}`}>Регистрация</NavLink></li>
            </>
          )     
          }
        </ul>
        </div>
      </div>
    </header>
  )
}
