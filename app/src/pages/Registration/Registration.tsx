import React from 'react'
import styles from './Registration.module.sass'
import { useState } from 'react';
import ReCAPTCHA from 'react-google-recaptcha';
import { set, useForm } from "react-hook-form"
import registrationSubmit from "../../api/registration"
import { ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Link } from 'react-router-dom'
import IRegistration from '../../interfaces/IRegistration';

export default function Registration() {
  const [isCaptchaSuccessful, setIsCaptchaSuccess] = useState(false)
  const {register, handleSubmit} = useForm<IRegistration>()
  const [modal, setModal] = useState(false)
  const [registrationStatus, setRegistrationStatus] = useState<number>(); // Добавленное состояние
  const [code, setCode] = useState('')
  

  const handleRegistration = async (data: IRegistration) => {
    const response = await registrationSubmit(data)
    console.log(response)
    setRegistrationStatus(response.status);
  };

  return (
  <>
    <ToastContainer />
    <form className={`modal-wrapper ${styles.registration}`} 
    onSubmit={handleSubmit(data => handleRegistration(data))
    }
    >
      <div className={styles.registration__wrapper}>
        <div className={`${styles.registration__left} ${styles.left}`}>
          <p className={`title ${styles.left__title}`}>Добро пожаловать!</p>
          <p className={`text ${styles.left__subtitle}`}>Чтобы оставаться с нами, пожалуйста войдите в свой аккаунт.</p>
          <Link to='/login' className={`button ${styles.left__button}`}>Войти</Link>
        </div>
        <div className={`${styles.registration__right} ${styles.right}`}>
          <p className={`title ${styles.right__title}`}>Создайте Аккаунт</p>
          <div className={`${styles.right__links}`}>
            <div className={`${styles.right__link} ${styles.right__link_border}`}>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="10" viewBox="0 0 16 10" fill="none">
                <path d="M15.3563 9.99919H13.6052C12.9427 9.99919 12.7431 9.43463 11.5554 8.18437C10.5175 7.13198 10.0791 7.00114 9.81658 7.00114C9.45346 7.00114 9.35443 7.10613 9.35443 7.63192V9.28925C9.35443 9.73751 9.21624 10 8.10307 10C7.02314 9.92367 5.9759 9.57852 5.0476 8.99297C4.11931 8.40741 3.33652 7.59822 2.76372 6.63203C1.40365 4.85115 0.457325 2.76096 0 0.527694C0 0.251472 0.099801 0.00109585 0.600341 0.00109585H2.3507C2.80057 0.00109585 2.96255 0.211897 3.13913 0.698919C3.98897 3.33029 5.43915 5.61922 6.02798 5.61922C6.25368 5.61922 6.35195 5.51422 6.35195 4.9222V2.21168C6.27748 0.975141 5.65334 0.870952 5.65334 0.423505C5.66124 0.305458 5.71256 0.195298 5.79642 0.116425C5.88028 0.0375521 5.99006 -0.00382026 6.10245 0.00109585H8.85388C9.23006 0.00109585 9.35443 0.198166 9.35443 0.671458V4.33019C9.35443 4.72513 9.51564 4.85598 9.62926 4.85598C9.85497 4.85598 10.0285 4.72513 10.4423 4.29061C11.3292 3.1526 12.0539 1.88471 12.5934 0.526886C12.6486 0.363862 12.753 0.224314 12.8906 0.129529C13.0282 0.034743 13.1916 -0.0100776 13.3557 0.00190345H15.1068C15.6319 0.00190345 15.7432 0.278125 15.6319 0.672266C14.995 2.17325 14.2069 3.59804 13.2812 4.9222C13.0924 5.22508 13.0171 5.38257 13.2812 5.73795C13.4547 6.01417 14.0689 6.55369 14.4811 7.06656C15.0815 7.69654 15.5797 8.42505 15.9566 9.22303C16.1071 9.7367 15.8561 9.99919 15.3563 9.99919Z" fill="black"/>
              </svg>
            </div>
            <div className={`${styles.right__link} ${styles.right__link_border}`}>
              <svg xmlns="http://www.w3.org/2000/svg" width="15" height="9" viewBox="0 0 15 9" fill="none">
                <path d="M13.1805 6.7487V4.9487H15V3.59926H13.1805V1.79926H11.817V3.59926H9.99825V4.9487H11.817V6.7487H13.1805ZM4.5465 1.75019C5.39766 1.75019 5.97085 2.11004 6.29689 2.41636L7.59053 1.17472C6.80323 0.446097 5.77628 2.05546e-07 4.5465 2.05546e-07C2.03886 -0.000743289 0 2.01561 0 4.49963C0 6.98364 2.03886 9 4.5465 9C7.17058 9 8.91271 7.17323 8.91271 4.60372C8.91271 4.22974 8.86463 3.96431 8.79777 3.68178H4.54425V5.35911H7.04738C6.92868 6.06617 6.28788 7.25948 4.5465 7.25948C3.04177 7.25948 1.81424 6.02156 1.81424 4.50558C1.81424 2.98736 3.04177 1.75019 4.5465 1.75019Z" fill="black"/>
              </svg>
            </div>
            <div className={`${styles.right__link}`}>
              <svg xmlns="http://www.w3.org/2000/svg" width="27" height="27" viewBox="0 0 27 27" fill="none">
                <path d="M1.28215 18.0562L5.23197 19.6885C5.46828 20.5588 5.9711 21.3363 6.67319 21.9104C7.44555 22.5418 8.41201 22.8886 9.41012 22.8925L9.41242 22.8925C9.98014 22.892 10.5422 22.78 11.0666 22.5627C11.591 22.3453 12.0674 22.0269 12.4685 21.6257C12.8697 21.2244 13.1877 20.7481 13.4044 20.224C13.6115 19.7234 13.7221 19.1886 13.731 18.6475L17.9822 15.6171C19.4512 15.6046 20.8575 15.0165 21.8972 13.9784C22.947 12.9304 23.5373 11.5092 23.5385 10.0268V10.0259C23.537 8.54361 22.9465 7.12261 21.897 6.07447C20.8475 5.02635 19.4246 4.4366 17.9404 4.43425H17.9396C14.8815 4.43425 12.3902 6.88963 12.3414 9.93273L9.35874 14.2436C8.59741 14.2514 7.85303 14.46 7.20042 14.8464L0.532144 12.0946C1.2326 5.57726 6.76134 0.5 13.4763 0.5C20.6695 0.5 26.5 6.32225 26.5 13.5C26.5 20.6791 20.6708 26.5 13.4777 26.5C7.89117 26.5 3.13168 22.9873 1.28215 18.0562Z" fill="black" stroke="black"/>
              </svg>
            </div>
          </div>
          <p className={`${styles.right__subtitle}`}>или используйте ваш email для регистрации</p>
          <div className={styles.registration__inputs}>
              <input placeholder='Логин' className={`${styles.registration__input} input`} type="text" {...register("username")}/>
              <input placeholder='Email' className={`${styles.registration__input} input`} type="email" {...register("email")}/>
              <input placeholder='7 (___) ___ - __ - __' className={`${styles.registration__input} input`} type="text" {...register("phoneNumber")}/>
              <input placeholder='Пароль' className={`${styles.registration__input} input`} type="password" {...register("password")}/>
              <input placeholder='Повторите пароль' className={`${styles.registration__input} input`} type="password" {...register("confirmPassword")}/>
            </div>
            <ReCAPTCHA className={styles.registration__captcha}
              sitekey="6LfUR4EnAAAAALkvTYM1IeiHLxfxIA1h5buGus6b"
              onChange={() => {setIsCaptchaSuccess(true)}}
            /> 
            <button type='submit' disabled={!isCaptchaSuccessful} className={`${styles.registration__button} button`}>
              Зарегистрироваться
            </button>
        </div>
      </div>

    </form>
  </>
  )
}
