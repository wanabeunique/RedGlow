import styles from './Headebook.module.sass'
import { Link, Routes, Route } from 'react-router-dom'
import HeadbookCiv5 from './HeadbookСiv5/HeadbookCiv5'  

export default function () {
  return (
    <div className={`container ${styles.headbook}`}>
      <ul className={styles.headbook__list}>
        <Link to='/headbook/headbook-civilization5' className={styles.headbook__item}>
          <img className={styles.headbook__img} src="/headbook/civ5.jpeg" alt="" />
        </Link>
        <Link to='/headbook/headbook-civilization6' className={styles.headbook__item}>
          <img className={styles.headbook__img} src="/headbook/civ6.png" alt="" />
        </Link>
      </ul>
      <Routes>
        <Route path='headbook-civilization5' element={<HeadbookCiv5/>}/>
      </Routes>
      {/* <HeadbookCiv5/> */}
    </div>

  )
}
