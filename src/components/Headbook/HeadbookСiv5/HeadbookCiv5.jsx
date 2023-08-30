import React, { useEffect, useState } from 'react';
import { Link, Routes, Route } from 'react-router-dom';
import styles from './HeadbookCiv5.module.sass';
import axios from 'axios';
import HeadbookCiv5Item from './HeadbookCiv5Item/HeadbookCiv5Item';


export default function () {
  const [input, setInput] = useState('');
  const [jsonData, setJsonData] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  
  useEffect(() => {
    const jsonFilePath = '/headbook/headbook_civilization5/allCivs.json';
    axios.get(jsonFilePath)
      .then(res => {
        setJsonData(res.data);
      })
      .catch(err => {
        console.error('Ошибка при запросе к JSON файлу', err);
      });
  }, []);
  
  return (
    <>
      <input
        className={`${styles.input} input`}
        placeholder="Введите нацию..."
        onChange={(event) => {
          setInput(event.target.value);
          console.log(input);
        }}
      />
      <div className={styles.headbook}>
        {jsonData ? (
          <div className={`text ${styles.nation}`}>
            {          
              Object.entries(jsonData).map(nation => (
                nation[0].toLowerCase().includes(input.toLowerCase()) ? (
                  <HeadbookCiv5Item key={nation[0]} nation={nation} className={styles.nation__item}/> 
                ) : null
              ))
            }
          </div>
        ) : (
          <p className='text'>Идет загрузка наций...</p>
        )}
      </div>
    </>
  );
}