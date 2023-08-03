import React, { useEffect, useState } from 'react'
import { Link, Routes, Route } from 'react-router-dom'
import styles from './HeadbookCiv5.module.sass'
import axios from 'axios'

export default function () {
  const [isModalVisible, setIsModalVisible] = useState('Аравия');
  const handleMouseEnter = (nation) => {
    setIsModalVisible(nation);
  }
  const handleMouseLeave = () => {
    setIsModalVisible(false)
  }
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
                console.log(nation)
                return(
                    <div 
                    className={`text ${styles.nation__item}`}
                    // onMouseEnter={handleMouseEnter(nation)}
                    // onMouseLeave={handleMouseLeave}
                    >
                    {nation[0]}
                    <img className={`text ${styles.nation__img}`} src={`/headbook/headbook_civilization5/${nation[1].Флаг}`} alt="" />
                    { isModalVisible == nation && (
                      <div className="modal">
                        <p>This is the modal content!</p>
                        <button onClick={() => setIsModalVisible(false)}>Close</button>
                      </div>
                    )}
                  </div>
                )
              })
            }
        </div>
            
            )
        
        :
        (<div>Загрузка данных</div>
        )
    }
    </div>

  )
}
