import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import styles from './EmailConfirm.module.sass';
import authService from '@/service/auth.service';

const confirmText = {
  200: 'Вы успешно Зарегистрированы!',
  400: 'Время действия истекло',
  403: 'Вы уже Зарегистрированы',
};

export default function EmailConfirm() {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const email = searchParams.get('email');
  const code = searchParams.get('code');
  const [status, setStatus] = useState(0);
  console.log(email, code)

  async function fetchData() {
    const response = await authService.confirmRegistration(email, code);
    console.log(response)
    setStatus(response);
  }

  useEffect(() => {
    if (email && code) {
      fetchData();
    }
  }, []);

  if (!status) return null;
  return <div className={styles.text}>{confirmText[status]}</div>;
}
