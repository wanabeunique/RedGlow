import React from 'react'
import styles from './Header.module.sass'

export default function Header() {
  return (
    <header className={styles.header}>
      <div className={`container ${styles.header__container}`}>
        <div className={styles.header__logo}>
          LOGO
        </div>
        <ul className={styles.header__items}>
          <li className={styles.header__item}><a href='#' className={`text ${styles.header__link}`}>Главная</a></li>
          <li className={styles.header__item}><a href='#' className={`text ${styles.header__link}`}>Играть</a></li>
          <li className={styles.header__item}><a href='#' className={`text ${styles.header__link}`}>Справочник</a></li>
          <li className={styles.header__item}><a href='#' className={`text ${styles.header__link}`}>Войти</a></li>
          {/* <li className={styles.header__item}>Профиль</li> */}
        </ul>
      </div>
    </header>
  )
}
