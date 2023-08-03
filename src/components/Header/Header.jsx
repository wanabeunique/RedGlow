import React from 'react'
import styles from './Header.module.sass'
import { Link } from 'react-router-dom'

export default function Header() {
  return (
    <header className={styles.header}>
      <div className={`container ${styles.header__container}`}>
        <div className={styles.header__logo}>
          LOGO
        </div>
        <ul className={styles.header__items}>
          <li className={styles.header__item}><Link to='/' className={`text ${styles.header__link}`}>Главная</Link></li>
          <li className={styles.header__item}><Link to='#' className={`text ${styles.header__link}`}>Играть</Link></li>
          <li className={styles.header__item}><Link to='/headbook' className={`text ${styles.header__link}`}>Справочник</Link></li>
          <li className={styles.header__item}><Link to='#' className={`text ${styles.header__link}`}>Войти</Link></li>
          {/* <li className={styles.header__item}>Профиль</li> */}
        </ul>
      </div>
    </header>
  )
}
