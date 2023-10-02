import React from 'react'
import styles from './NotFound.module.sass'
import {Link} from 'react-router-dom'

export default function NotFound() {
  return (
    <div className={styles.notFound}>
      <div className={styles.notFound__text}>Страница не найдена</div>
      <Link className={styles.notFound__link} to={'/'}>Перейти на главную страницу</Link>
    </div>
  )
}
