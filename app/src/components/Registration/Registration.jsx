import React from 'react'
import styles from './Registration.module.sass'
import { useState } from 'react';
import ReCAPTCHA from 'react-google-recaptcha';
import { set, useForm } from "react-hook-form"
import registrationSubmit from "./../../api/registration"
import { ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default function Registration() {
  const [isCaptchaSuccessful, setIsCaptchaSuccess] = useState(false)
  const {register, handleSubmit} = useForm()
  const [modal, setModal] = useState(false)
  const [registrationStatus, setRegistrationStatus] = useState(null); // Добавленное состояние
  const [code, setCode] = useState('')
  

  const handleRegistration = async (data) => {
    const response = await registrationSubmit(data)
    console.log(response)
    setRegistrationStatus(response.status);
  };

  return (
  <>
    <ToastContainer />
    <form className={styles.registration} 
    onSubmit={handleSubmit(data => handleRegistration(data))
    }
    >
      <div className={styles.registration__wrapper}>
        <p className={`${styles.registration__title} title`}>Регистрация</p>
        <p className={`${styles.registration__subtitle} subtitle`}>Логин</p>
        <input className={`${styles.registration__input} input`} type="text" {...register("username")}/>
        <p className={`${styles.registration__subtitle} subtitle`}>Электронная почта</p>
        <input className={`${styles.registration__input} input`} type="email" {...register("email")}/>
        <p className={`${styles.registration__subtitle} subtitle`}>Номер телефона</p>
        <input className={`${styles.registration__input} input`} type="text" placeholder='+7 (___) ___ - __ - __' {...register("phoneNumber")}/>
        <p className={`${styles.registration__subtitle} subtitle`}>Пароль</p>
        <input className={`${styles.registration__input} input`} type="password" {...register("password")}/>
        <p className={`${styles.registration__subtitle} subtitle`}>Повторить пароль</p>
        <input className={`${styles.registration__input} input`} type="password" {...register("confirmPassword")}/>
        <ReCAPTCHA className={styles.registration__captcha}
          sitekey="6LfUR4EnAAAAALkvTYM1IeiHLxfxIA1h5buGus6b"
          onChange={() => {setIsCaptchaSuccess(true)}}
        /> 
        <button type='submit' disabled={!isCaptchaSuccessful} className={`${styles.registration__button} button`}>
          Зарегистрироваться
        </button>
      </div>
    </form>
  </>
  )
}
