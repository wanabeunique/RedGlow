import styles from "./Login.module.sass";
import { Link } from "react-router-dom";
import login from "../../api/login";
import { useForm } from "react-hook-form";
import { Navigate } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "../../hooks";
import ILogin from "../../interfaces/ILogin";

export default function Login() {
  const dispatch = useAppDispatch();
  const isAuth = useAppSelector((state) => state.authReducer.data);
  const { register, handleSubmit } = useForm<ILogin>();

  if (!isAuth) {
    return (
      <form
        className={styles.login}
        onSubmit={handleSubmit((data) => login(data, dispatch))}
      >
        <div className={`modal-wrapper ${styles.login__wrapper}`}>
          <div className={styles.left}>
            <p className={`title ${styles.left__title}`}>Войдите</p>
            <div className={`${styles.left__links}`}>
            </div>
            <p className={styles.left__subtitle}>или используйте ваш аккаунт</p>
            <div className={styles.left__inputs}>
              <input
                placeholder="Логин"
                className={`${styles.login__input} auth-input`}
                type="text"
                {...register("username")}
              />
              <input
                placeholder="Пароль"
                className={`${styles.login__input} auth-input`}
                type="text"
                {...register("password")}
              />
            </div>
            <Link
              to={"/recovery"}
              className={`text ${styles.login__link} ${styles.left__subtitle}`}
            >
              Забыл Пароль?
            </Link>
            <button
              type="submit"
              className={`${styles.left__button} auth-button`}
            >
              Войти
            </button>
          </div>
          <div className={styles.right}>
            <p className={`${styles.right__title} title`}>Привет, друг!</p>
            <p className={`${styles.right__subtitle} text`}>
              Создай свой аккаунт, чтобы присоединиться к нам
            </p>
            <Link
              to={"/registration"}
              className={`auth-button ${styles.right__button}`}
            >
              Зарегистрироваться
            </Link>
          </div>
        </div>
      </form>
    );
  } else {
    return <Navigate to="/" />;
  }
}
