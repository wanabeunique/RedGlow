import React, { useEffect, useState } from 'react'
import { Link, Routes, Route } from 'react-router-dom'
import styles from './HeadbookCiv5.module.sass'
import axios from 'axios'
import HeadbookCiv5Item from './HeadbookCiv5Item/HeadbookCiv5Item';

export default function () {
  const [jsonData, setJsonData] = useState(null)
  console.log('я тут')
  useEffect(() => {
    const jsonFilePath = '/headbook/headbook_civilization5/allCivs.json';
    axios.get(jsonFilePath)
      .then(res => {
        setJsonData(res.data);
      })
      .catch(err => {
        console.error('Ошибка при запросе к JSON файлу', err);
      }); // Закрываем круглую скобку здесь
  }, []);
  
  return (
    <div className={styles.headbook}>
      {jsonData ? (
          <div className={`text ${styles.nation}`}>
            {          
              Object.entries(jsonData).map(nation => {
                return(
                    <HeadbookCiv5Item key={nation[0]} nation={nation}/> 
                )
              })
            }
        </div>
            
            )
        
        :
        (<p className='text'>Идет загрузка наций...</p>
        )
    }
    </div>

  )
}
