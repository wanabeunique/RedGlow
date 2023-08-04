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
        {nationName}
        <img className={`text ${styles.item__img}`} src={nationImgSource} alt="" />
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
