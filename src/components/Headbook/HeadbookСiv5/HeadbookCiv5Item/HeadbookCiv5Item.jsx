import React, { useState } from 'react';
import styles from './HeadbookCiv5Item.module.sass';

export default function HeadbookCiv5Item({ nation }) {
  const nationName = nation[0];
  const nationImgSource = `/headbook/headbook_civilization5/${nation[1].Флаг}`;
  const nationLeaderName = Object.keys(nation[1].Лидер[0])[1];
  const nationLeaderBonus = Object.values(nation[1].Лидер[0])[1].Персоналия;
  const nationLeaderImg = `/headbook/headbook_civilization5/${Object.values(nation[1].Лидер[0])[0]}`;
  const nationBuilding = nation[1]["Уникальное здание"] || nation[1]["Уникальная постройка"] || null;
  const nationUnit = nation[1]["Уникальный юнит"] || null;
  const [toggle, setToggle] = useState(false);

  return (
    <div className={`text ${styles.item}`} onClick={() => { setToggle(!toggle) }}>
      <div className={styles.item__top}>
        <p className='text'>{nationName}</p>
        <img className={`text ${styles.item__img}`} src={nationImgSource} alt="" />
        <svg className={toggle ? styles.active : ''} width="50px" height="50px" viewBox="0 0 24 24" fill="#999" xmlns="http://www.w3.org/2000/svg">
        <path d="M5.70711 9.71069C5.31658 10.1012 5.31658 10.7344 5.70711 11.1249L10.5993 16.0123C11.3805 16.7927 12.6463 16.7924 13.4271 16.0117L18.3174 11.1213C18.708 10.7308 18.708 10.0976 18.3174 9.70708C17.9269 9.31655 17.2937 9.31655 16.9032 9.70708L12.7176 13.8927C12.3271 14.2833 11.6939 14.2832 11.3034 13.8927L7.12132 9.71069C6.7308 9.32016 6.09763 9.32016 5.70711 9.71069Z" fill="#999"/>
        </svg>
      </div>
      {toggle ? (
        <div className={styles.content}>
          <div className={styles.content__item}>
            <p className='text'>Лидер:</p>
            <p className='text'>{nationLeaderName}</p>
          </div>
          <img className={styles.content__leaderImg} src={nationLeaderImg} alt="" />
          <div className={styles.content__bonus}>
            <p className='text'>Уникальный бонус:</p>
            <p className='text'>{nationLeaderBonus}</p>
          </div>
          {nationBuilding ? (
            <div className={styles.content__bulding}>
              <p>Уникальное здание:</p>
              <div className={styles.content__buildingWrapper}>
                <p>{Object.keys(nationBuilding[0])[1]}</p>
                <img className={styles.content__buildingImg} src={`/headbook/headbook_civilization5/${nationBuilding[0].image}`} />
              </div>
              <p className='text'>Замещает: {Object.values(nationBuilding[0])[1]['Замещает']}</p>
              <p className='text'>Эффект: {Object.values(nationBuilding[0])[1]['Эффект']}</p>
            </div>
          ) : (
              <p>Уникальное здание отсутствует</p>
            )}
          {nationUnit ? (
            nationUnit.map(el => (
              <div key={Object.keys(el)[1]}>
                <div className={styles.content__unit}>
                  <p className='text'>{Object.keys(el)[1]}</p>
                  <img className={styles.content__unitImg} src={`/headbook/headbook_civilization5/${el.image}`} alt="" />
                </div>
                <p className='text'>Замещает: {Object.values(el)[1]['Замещает']}</p>
                <p className='text'>Эпоха: {Object.values(el)[1]['Эпоха']}</p>
                <p className='text'>Сила: {Object.values(el)[1]['Сила'] || Object.values(el)[1]['Дальний бой']}</p>
              </div>
            ))
          ) : (
              <p>Уникальный юнит отсутствует</p>
            )}
        </div>
      ) : null}
    </div>
  );
}
