import { useEffect, useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import recoveryPassword from '../../api/recoveryPassword';
import styles from './Recovery.module.sass';
import { Navigate, useNavigate, useSearchParams } from 'react-router-dom';
import setForgotPassword from '@/api/setForgotPassword';

export default function RecoveryNewPassword() {
  const [password, setPassword] = useState('');
  const [searchParams] = useSearchParams();
  const code = searchParams.get('code');
  const email = searchParams.get('email');

  if (!email || !code) return <Navigate to="/404" />;

  
  return (
    <div className={`contaier ${styles.container}`}>
      <p className={`title`}>Введите новый пароль</p>
      <Input
        placeholder="Новый пароль"
        className={`input`}
        type="mail"
        value={password}
        onChange={(e) => {
          setPassword(e.target.value);
        }}
      />
      <Button
        className="button"
        onClick={() => {
          setForgotPassword(password, email, code);
        }}
      >
        Отправить
      </Button>
    </div>
  );
}
