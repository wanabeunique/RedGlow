import React from 'react'
import styles from './Login.module.sass'
import { Link, Routes } from 'react-router-dom'

export default function Login() {
  return (
    <form className={styles.login}>
      <div className={styles.login__wrapper}>
        <p className={`${styles.login__title} title`}>Авторизация</p>
        <p className={`${styles.login__subtitle} subtitle`}>Логин</p>
        <input className={`${styles.login__input} input`} type="text" />
        <p className={`${styles.login__subtitle} subtitle`}>Пароль</p>
        <input className={`${styles.login__input} input`} type="text" />
        <button type='submit' className={`${styles.login__button} button`}>Войти</button>
        <div className={styles.login__reg}>
          <p className='text'>Нет аккаунта?</p>
          <Link to={'/registration'} className={`text ${styles.login__link}`}>Зарегистрироваться</Link>
        </div>
      </div>
      {/* <Routes>  
        <Route ></Route>
      </Routes> */}
    </form>
  )
}
