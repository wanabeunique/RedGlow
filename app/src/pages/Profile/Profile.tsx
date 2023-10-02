import React from 'react'
import styles from './Proflie.module.sass'
import Avatar from 'antd/es/avatar/avatar'
import {  Button, Modal  } from 'antd'
import { useState } from 'react'
import getProfile from '../../api/getProfile'
import { useEffect } from 'react'
import IUser from '../../interfaces/IProfile'


export default function Profile() {
  const [user, setUser] = useState<IUser>()

  const [isModalOpen, setIsModalOpen] = useState(false);
  useEffect(() => {
    const getUser = async () => {
      const userData = await getProfile()
      setUser(userData)
    }
    getUser()
  }, [])

  const showModal = () => {
    setIsModalOpen(true);
  };
  const handleOk = () => {
    setIsModalOpen(false);
  };
  const handleCancel = () => {
    setIsModalOpen(false);
  };
  
  return (
    <div className={`${styles.profile}`}>
      <div className={styles.profile__top}> 
        <img className={styles.profile__top_bg} src='./../../src/assets/profile-bg.jpg' alt="" />
        <div className={`container ${styles.profile__top_wrapper}`}>
          <div className={styles.profile__top_avatar}>
            <Avatar size={160} />
          </div>
          <div className={styles.profile__top_text}>
            <p className={`${styles.profile__top_nickname} title`}>
              {
                user?
                (<span>{user.username}</span>)
                :null
              }
            </p>
            <p className={`${styles.profile__top_registratedTime} text`}>На сайте с 03.01.2005</p>
          </div>
        </div>
      </div>
      <div className={`container ${styles.profile__content}`}>
        <div className={`${styles.profile__settings} ${styles.settings}`}>
          <div className={styles.settings__change_password}>     
            {
              user? (
              <div>
                <p className='text'>{user.phoneNumber}</p>
                <p className='text'>{user.email}</p>
                <p className='text'>{user.decency}</p>
                <p className='text'>{user.reports}</p>
                <p className='text'>{user.subExpiresIn}</p>
              </div>
              ):null     
            }
            <Button type="primary" onClick={showModal}>
              Изменить пароль
            </Button>
            <Modal title="Basic Modal" open={isModalOpen} onOk={()=> {handleOk; alert('Пароль изменен')}} onCancel={handleCancel}>
              <p className='text'>Введите текущий пароль:</p>
              <input className='input' type="text" />
              <p className='text'>Введите новый пароль:</p>
              <input className='input' type="password" />
              <p className='text'>Повторите новый пароль:</p>
              <input className='input' type="password" />
            </Modal>
          </div>
        </div>
      </div>
    </div>
  )
}
