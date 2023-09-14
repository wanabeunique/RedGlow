import React, { useEffect } from 'react'
import styles from './Friends.module.sass'
import { useSelector } from 'react-redux'
import getUserFriends from '../../api/getUserFriends'

export default function Friends() {
  const username = useSelector(state => state.userReducer.username)
  return (
    <div className='container'>
      <div className={styles.search}>
        <input type="text" placeholder='Добавление в друзья'/>
      </div>
      <div className="list">
        <button onClick={() => {getUserFriends(username)}}>Получить друзей</button>
        {

        }
      </div>
    </div>
  )
}
