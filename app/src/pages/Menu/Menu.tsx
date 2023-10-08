import { NavLink } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "../../hooks";
import styles from "./Menu.module.sass";
import { setProfileMenuActive } from "../../store/reducers/isMenusActiveSlice";

export default function Menu() {
  const isProfileActive = useAppSelector((state) => state.menusReduce.profile);
  const dispatch = useAppDispatch()

  function HandleNavigate(){
    dispatch(setProfileMenuActive(false))
  }

  return (
    <div className={`${styles.menu} ${isProfileActive ? styles.menu_active : null}`}>
      <div className={styles.menu__wrapper}>
        <div className={styles.menu__group}>
          <NavLink onClick={() => {HandleNavigate()}} to="/Generate" className={`${styles.menu__title} ${styles.menu__link_white}`}>
            Генерация наций
          </NavLink>
        </div>
        <div className={styles.menu__group} >
          <NavLink to="/headbook" className={`${styles.menu__title} ${styles.menu__link_white}`}>
            Справочник
          </NavLink>
        </div>

        
        <div className={styles.menu__group}>
          <p className={styles.menu__title}>История игр</p>
          <div className={styles.menu__items}>
            <a href="#" className={`${styles.menu__item} ${styles.menu__link_red}`}>Civilization 5</a>
            <a href="#" className={`${styles.menu__item} ${styles.menu__link_red}`}></a>
            <a href="#" className={`${styles.menu__item} ${styles.menu__link_red}`}></a>
          </div>
        </div>
        <div className={styles.menu__group}>
          <p className={styles.menu__title}>Безопасность</p>
          <div className={styles.menu__items}>
            <a href="#" className={`${styles.menu__item} ${styles.menu__link_red}`}>Смена данных</a>
            <a href="#" className={`${styles.menu__item} ${styles.menu__link_red}`}>Двухэтапная аунтификация</a>
            <a href="#" className={`${styles.menu__item} ${styles.menu__link_red}`}>Привязка телефона</a>
          </div>
        </div>
      </div>
    </div>
  );
}
