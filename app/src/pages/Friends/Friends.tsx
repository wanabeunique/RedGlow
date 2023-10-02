import React, { useEffect, useState } from 'react'
import styles from './Friends.module.sass'
import { useSelector } from 'react-redux'
import getUserFriends from '../../api/getUserFriends'
import sendFriendRequest from '../../api/sendFriendRequest'
import getUsersByValue from '../../api/getUsersByValue'
import { RootState } from '../../store/store'
import IUsername from '../../interfaces/IUsername'
import { useDebounce } from '../../hooks'

export default function Friends() {
  const username: string = useSelector((state: RootState) => state.userReducer.username)
  const [searchedUsers, setSearchedUsers] = useState<Array<string>>([])
  const [friendsData, setFriendsData] = useState<any>([])
  const [queryNickname, setQueryNickname] = useState('')
  const debouncedSearchUsers = useDebounce(queryNickname)
  
  useEffect(() => {
    async function getSearchedUsers() {
      if (queryNickname.length > 2) {
        async function getRequest(){
          await getUsersByValue(debouncedSearchUsers)
            .then(res => {
              setSearchedUsers(res)
            })
        }
        getRequest()
      }

      else{
        setSearchedUsers([])
      }
    }
    getSearchedUsers()
  }, [debouncedSearchUsers])


  useEffect(() => {
    const friends = async () => {
      const friendsDataValue: Array<string> = await getUserFriends(username)
      setFriendsData(friendsDataValue)
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
          setSearchedUsers
          }}
          value={queryNickname} 
          className={`${styles.search__input} input`} 
          type="text" 
          placeholder='Введите имя друга...'/>
        <button onClick= {() => {sendFriendRequest(queryNickname)}} className={`${styles.search__button} button`}>Отправить заявку</button>
      </div>
      <div className={`${styles.list_search}`}>
        <>
        {searchedUsers.map((user: any) => (
                <div className={`${styles.friends__item} friend`}>
                  <p className={`${styles.friends__title} text`}>{user.username}</p>
                  <div className={styles.friends__tools}>
                    <div className={styles.friends__chat}>
                      <svg width="40px" height="40px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M17 3.33782C15.5291 2.48697 13.8214 2 12 2C6.47715 2 2 6.47715 2 12C2 13.5997 2.37562 15.1116 3.04346 16.4525C3.22094 16.8088 3.28001 17.2161 3.17712 17.6006L2.58151 19.8267C2.32295 20.793 3.20701 21.677 4.17335 21.4185L6.39939 20.8229C6.78393 20.72 7.19121 20.7791 7.54753 20.9565C8.88837 21.6244 10.4003 22 12 22C17.5228 22 22 17.5228 22 12C22 10.1786 21.513 8.47087 20.6622 7" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/>
                        <path d="M8 12H8.009M11.991 12H12M15.991 12H16" stroke="#1C274C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </div>
                    <div className={styles.friend__remove}>
                      <svg fill="#000000" width="40px" height="40px" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M1,20a1,1,0,0,0,1,1h8a1,1,0,0,0,0-2H3.071A7.011,7.011,0,0,1,10,13a5.044,5.044,0,1,0-3.377-1.337A9.01,9.01,0,0,0,1,20ZM10,5A3,3,0,1,1,7,8,3,3,0,0,1,10,5Zm12.707,9.707L20.414,17l2.293,2.293a1,1,0,1,1-1.414,1.414L19,18.414l-2.293,2.293a1,1,0,0,1-1.414-1.414L17.586,17l-2.293-2.293a1,1,0,0,1,1.414-1.414L19,15.586l2.293-2.293a1,1,0,0,1,1.414,1.414Z"/></svg>
                    </div>
                  </div>
                </div>
                )
              )}
        </>
      </div>
      <div className={`${styles.list}`}>
        <p className='title'>Список друзей:</p>
        {friendsData ?
          (
            <div className={styles.friends__items}>
              {friendsData.map((friend: IUsername) => (
                <div className={`${styles.friends__item} friend`}>
                  <p className={`${styles.friends__title} text`}>{friend.username}</p>
                  <div className={styles.friends__tools}>
                    <div className={styles.friends__chat}>
                      <svg width="40px" height="40px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M17 3.33782C15.5291 2.48697 13.8214 2 12 2C6.47715 2 2 6.47715 2 12C2 13.5997 2.37562 15.1116 3.04346 16.4525C3.22094 16.8088 3.28001 17.2161 3.17712 17.6006L2.58151 19.8267C2.32295 20.793 3.20701 21.677 4.17335 21.4185L6.39939 20.8229C6.78393 20.72 7.19121 20.7791 7.54753 20.9565C8.88837 21.6244 10.4003 22 12 22C17.5228 22 22 17.5228 22 12C22 10.1786 21.513 8.47087 20.6622 7" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/>
                        <path d="M8 12H8.009M11.991 12H12M15.991 12H16" stroke="#1C274C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </div>
                    <div className={styles.friend__remove}>
                      <svg fill="#000000" width="40px" height="40px" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M1,20a1,1,0,0,0,1,1h8a1,1,0,0,0,0-2H3.071A7.011,7.011,0,0,1,10,13a5.044,5.044,0,1,0-3.377-1.337A9.01,9.01,0,0,0,1,20ZM10,5A3,3,0,1,1,7,8,3,3,0,0,1,10,5Zm12.707,9.707L20.414,17l2.293,2.293a1,1,0,1,1-1.414,1.414L19,18.414l-2.293,2.293a1,1,0,0,1-1.414-1.414L17.586,17l-2.293-2.293a1,1,0,0,1,1.414-1.414L19,15.586l2.293-2.293a1,1,0,0,1,1.414,1.414Z"/></svg>
                    </div>
                  </div>
                </div>
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
