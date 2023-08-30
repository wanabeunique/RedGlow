import React from 'react'
import styles from './Header.module.sass'
import { Link, NavLink } from 'react-router-dom'
import { Avatar } from 'antd'

export default function Header() {
  const nickname = 'wanabeunique'
  return (
    <header className={styles.header}>
      <div className={`container ${styles.header__container}`}>
        <Link to={'/'} className={styles.header__logo}>
          LOGO
        </Link>
        <ul className={styles.header__items}>
          <li className={styles.header__item}><NavLink to='/' className={`text ${styles.header__link}`}>Главная</NavLink></li>
          <li className={styles.header__item}><NavLink to='/Generate' className={`text ${styles.header__link}`}>Генерация наций</NavLink></li>
          <li className={styles.header__item}><NavLink to='/Friends' className={`text ${styles.header__link}`}>Друзья</NavLink></li>
          <li className={styles.header__item}><NavLink to='/Play' className={`text ${styles.header__link}`}>Играть</NavLink></li>
          <li className={styles.header__item}><NavLink to='/headbook' className={`text ${styles.header__link}`}>Справочник</NavLink></li>
          <li className={styles.header__item}><NavLink to='/Login' className={`text ${styles.header__link}`}>Войти</NavLink></li>
          <li className={styles.header__item}><NavLink to='/Registration' className={`text ${styles.header__link}`}>Регистрация</NavLink></li>
          <li className={`${styles.header__item}`}><NavLink to='/Profile' className={`text ${styles.header__link} ${styles.header__profile}`}>
            <p className='text'>{nickname}</p>
            <Avatar />
          </NavLink></li>
        </ul>
      </div>
    </header>
  )
}
