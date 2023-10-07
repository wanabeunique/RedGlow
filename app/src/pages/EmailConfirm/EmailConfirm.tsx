import React, { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom';
import validateCode from '../../api/validateCode';
import styles from './EmailConfirm.module.sass'


export default function EmailConfirm() {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const key: string | null  = searchParams.get('key');
  const code: string | null = searchParams.get('code');
  const [status, setStatus] = useState<number>();

  useEffect(() => {
    async function fetchData(){
      if (key && code){
        const response = await validateCode(code, key)
        console.log(response.status)
        setStatus(response.status)
        console.log(status)
      }
    }
    fetchData()
  }, [])

  if (status == 200){
    return <div className={styles.text}>Вы успешно Зарегистрированы!</div>
  }
  if (status == 400){
    return <div className={styles.text}>Время действия истекло</div>
  }
  if (status == 403){
    return <div className={styles.text}>Вы уже Зарегистрированы</div>
  }
  else if (status){
    return <div className={styles.text}>Неизвестная ошибка</div>
  }
}
