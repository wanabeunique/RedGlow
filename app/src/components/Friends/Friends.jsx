import React, { useEffect, useState } from 'react'
import styles from './Friends.module.sass'
import { useSelector } from 'react-redux'
import getUserFriends from '../../api/getUserFriends'
import sendFriendRequest from '../../api/sendFriendRequest'

export default function Friends() {
  const username = useSelector(state => state.userReducer.username)
  let friendsData = []
  const [queryNickname, setQueryNickname] = useState('')
  
  useEffect(() => {
    const friends = async () => {
      friendsData = await getUserFriends(username)
    }
    friends()
  }, [])

  return (
    <div className={`container ${styles.friends}`}>
      <div className={styles.search}>
        <input onChange={() => {setQueryNickname(event.target.value)}} value={queryNickname} className={`${styles.search__input} input`} type="text" placeholder='Введите имя друга...'/>
        <button onClick= {() => {sendFriendRequest(queryNickname)}} className={`${styles.search__button} button`}>Отправить заявку</button>
      </div>
      <div className={`${styles.list}`}>
        <p className='title'>Список друзей:</p>
        {friendsData.length?
          (
            <div>
              {`У вас есть друзья :)))))`}
            </div>
          ):(
            <p className='text'>
              {`У вас нет друзей :(`}
            </p>
          )
        }
      </div>
    </div>
  )
}
