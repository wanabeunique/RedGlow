import React from 'react'
import styles from './Login.module.sass'
import { Link, Routes } from 'react-router-dom'
import login from '../../api/login'
import {useForm } from "react-hook-form"

export default function Login() {
  const {register, handleSubmit} = useForm()
  return (
    <form 
      className={styles.login} 
      onSubmit={handleSubmit(data => login(data))}
    >
      <div className={styles.login__wrapper}>
        <p className={`${styles.login__title} title`}>Авторизация</p>
        <input placeholder='Логин' className={`${styles.login__input} input`} type="text" {...register("username")}/>
        <input placeholder='Пароль' className={`${styles.login__input} input`} type="text" {...register("password")}/>
        <button type='submit' className={`${styles.login__button} button`}>Войти</button>
        <div className={styles.login__reg}>
          <p className='text'>Нет аккаунта?</p>
          <Link to={'/registration'} className={`text ${styles.login__link}`}>Зарегистрироваться</Link>
        </div>
      </div>
    </form>
  )
}
