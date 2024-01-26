import styles from './Recovery.module.sass';
import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import passwordService from '@/service/password.service';

export default function Recovery() {
  const [email, setEmail] = useState('');
  return (
    <div className={`contaier ${styles.container}`}>
      <p className={styles.title}>Восстановление пароля</p>
      <Input
        placeholder="Введите email"
        type="mail"
        value={email}
        onChange={(e) => {
          setEmail(e.target.value);
        }}
      />
      <Button
        onClick={() => {
          passwordService.sendPasswordResetLink(email);
        }}
      >
        Отправить
      </Button>
    </div>
  );
}
