import React from "react";
import { useState } from "react";
import recoveryPassword from "../../api/recoveryPassword";
import styles from "./Recovery.module.sass";
import { useLocation } from "react-router-dom";

export default function Recovery() {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const key = searchParams.get("key");
  const [password, setPassword] = useState("");
  return (
    <div className={`contaier ${styles.container}`}>
      <p className={`title`}>Введите новый пароль</p>
      <input
        placeholder="Новый пароль"
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
          recoveryPassword(password);
        }}
      >
        Отправить
      </button>
    </div>
  );
}
