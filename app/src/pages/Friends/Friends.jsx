import React, { useEffect, useState } from 'react'
import styles from './Friends.module.sass'
import { useSelector } from 'react-redux'
import getUserFriends from '../../api/getUserFriends'
import sendFriendRequest from '../../api/sendFriendRequest'
import getUsersByValue from '../../api/getUsersByValue'


export default function Friends() {
  function setUsersByValue(value){
    // TODO: Всегда приходит пустая строка
    let res
    const search = async (value) => {
      res = await getUsersByValue(value)
      console.log(res)
      setSearchedUsers(res)
    }
    search(value)
    console.log(searchedUsers, `:Найденные юзеры`)
  }

  const username = useSelector(state => state.userReducer.username)
  
  const [searchedUsers, setSearchedUsers] = useState([])
  const [friendsData, setFriendsData] = useState([])

  const [queryNickname, setQueryNickname] = useState('')
  
  useEffect(() => {
    const friends = async () => {
      const friendsDataValue = await getUserFriends(username)
      setFriendsData(friendsDataValue.data)
    }
    friends()
    console.log(friendsData)
  }, [])

  return (
    <div className={`container ${styles.friends}`}>
      <div className={styles.search}>
        <input onChange={
          (event) => {
          setQueryNickname(event.target.value);
          setUsersByValue(queryNickname)
          }}
          value={queryNickname} 
          className={`${styles.search__input} input`} 
          type="text" 
          placeholder='Введите имя друга...'/>
        <button onClick= {() => {sendFriendRequest(queryNickname)}} className={`${styles.search__button} button`}>Отправить заявку</button>
      </div>
      <div className={`${styles.list}`}>
        <p className='title'>Список друзей:</p>
        {friendsData ?
          (
            <div>
              {friendsData.map((friend) => (
                <div className='text'>{friend.username}</div>
                )
              )}
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
