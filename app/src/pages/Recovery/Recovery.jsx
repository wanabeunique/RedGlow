import React from "react";
import { useState } from "react";
import recoveryPassword from "../../api/recoveryPassword.ts";
import styles from "./Recovery.module.sass";

export default function Recovery() {
  const [email, setEmail] = useState("");
  return (
    <div className={`contaier ${styles.container}`}>
      <p className={`title`}>Восстановление пароля</p>
      <input
        placeholder="Введите email"
        className={`input`}
        type="mail"
        value={email}
        onChange={() => {
          setEmail(event.target.value);
        }}
      />
      <button
        className="button"
        onClick={() => {
          recoveryPassword(email);
        }}
      >
        Отправить
      </button>
    </div>
  );
}
