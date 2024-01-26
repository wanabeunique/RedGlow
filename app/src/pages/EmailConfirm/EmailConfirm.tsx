import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import styles from './EmailConfirm.module.sass';
import authService from '@/service/auth.service';

export default function EmailConfirm() {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const email: string | null = searchParams.get('email');
  const code: string | null = searchParams.get('code');
  const [status, setStatus] = useState<number>();

  useEffect(() => {

    async function fetchData() {
      if (email && code) {
        const response = await authService.confirmRegistration(code, email);
        setStatus(response.status);
      }
    }
    fetchData();
  }, []);

  switch(status){
    case 200:
      return <div className={styles.text}>Вы успешно Зарегистрированы!</div>;
    case 400:
      return <div className={styles.text}>Время действия истекло</div>;
    case 403:
      return <div className={styles.text}>Вы уже Зарегистрированы</div>;
    default:
      return <div className={styles.text}>Неизвестная ошибка</div>;
  }
}
