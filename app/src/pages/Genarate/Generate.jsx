import { useState } from 'react'
import styles from './Generate.module.sass'
import { useEffect } from 'react'
import axios from 'axios'
import HeadbookCiv5Item from '../Headbook/HeadbookСiv5/HeadbookCiv5Item/HeadbookCiv5Item'
import { toast } from "react-toastify";
import { ToastContainer} from 'react-toastify';

export default function Generate() {
  const [gameStage, setGameStage] = useState('')
  const [startGame, setStartGame] = useState(false)
  const [playerName, setPlayerName] = useState('')
  const [playersList, setPlayersList] = useState([])
  const [jsonData, setJsonData] = useState(null);
  
  const [usedNations, setUsedNations] = useState([]) 
  const [bans, setBans] = useState([])
  const [autoBans, setAutoBans] = useState([])

  const [currentPlayer, setCurrentPlayer] = useState(0)
  const [currentAction, setCurrentAction] = useState('')

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
  
  function addPlayer(){
    if (!playerName){
      toast.error('Имя игрока должно содержать хотя бы 1 символ')
      return
    }
    setPlayersList(prevPlayersList => [...prevPlayersList, playerName])
    setPlayerName('')
  }

  function switchPlayers(){
    if (playersList.length < 2) {
      toast.error('Введите хотя бы 2х игроков')
      return
    }
    let array = [...playersList]
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    console.log(array)
    setPlayersList(array)
  }

  function beginGame(){
    if (playersList.length < 2) {
      toast.error('Введите хотя бы 2х игроков')
      return
    }
    setStartGame(true)
    setCurrentAction('убирает любую нацию')
    setGameStage(1)
  }

  useEffect(() => {
    if(autoBans.length == playersList.length && autoBans.length){
      getRandomNations()
    }
  }, [autoBans])

  function getRandomNations(){
    console.log(autoBans)
    let nations = []
    Object.entries(jsonData).map(nation => {
      nations.push(nation)
    })
    console.log(nations)
    for (let i = nations.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [nations[i], nations[j]] = [nations[j], nations[i]];
    }
    console.log(nations)
    nations.forEach((nation, i) => {
      autoBans.forEach(ban => {
        if (nation[0] == ban[0]){
          nations.splice(i, 1)
        }
      })
    })
    console.log(nations)
    const deletedNations = nations.slice(playersList.length * 4, nations.length)
    console.log(nations)
    setUsedNations([...usedNations, ...deletedNations])
  }

  async function pick(nation){
    setUsedNations([...usedNations, nation])
    if (gameStage == 1){
      setAutoBans([...autoBans, nation])
    }
    if (gameStage == 2){
      setBans([...bans, nation])
    }
    if (gameStage == 3){
      setCurrentAction('выбират нацию')
    }
    if(currentPlayer + 1 != playersList.length)
    {
      setCurrentPlayer(currentPlayer + 1)
    }
    else{
      setGameStage(gameStage + 1)
      setCurrentPlayer(0)
      if (gameStage + 1 == 3){
        setCurrentAction('выбирает нацию')
      }
    }
    
  }

  return (
    <>
      <ToastContainer />
      <div className='container'>
        <div className={`${styles.top}`}>
          <p className="text">Список игроков:</p>
          <div className={`${styles.players__list} ${startGame ? styles.active : ''} `}>
            {
              playersList.map( (player,i) => (
                <p className={`${styles.player} text`}>{i+1}. {player}</p>
              ))
            }
          </div>
          {
            startGame ? '' :
            <button 
              className={`${styles.switch} text`} 
              onClick={
                () => {switchPlayers()}
              }>Перемешать игроков
            </button>
          }
        </div>
        <div className={styles.add}>
          {
            startGame ? '' :
            (
              <>
                <input 
                  type="text" 
                  className={`input ${styles.add__input}`}
                  value={playerName} 
                  onChange={() => {setPlayerName(event.target.value)}} 
                  placeholder='Введите игрока..'
                />
                <button className={styles.add__button} onClick={() => {addPlayer()}}>Добавить игрока</button>
                <button className={styles.add__button} onClick={() => 
                  beginGame()
                  }>Запустить игру
                </button>
              </>
            )
          }
        </div>
        {
          currentAction ? (
            <div className={`text ${styles.action}`}>
            Игрок {playersList[currentPlayer]} {currentAction}
          </div>
          ) : ''
        }
        <div className={styles.content}>
          <div className={styles.actions}>
            <div className={`${styles.autobans} ${styles.action}`}>
              <p className="title">Автобаны:</p>
              {
                autoBans.map(nation => (
                  <HeadbookCiv5Item key={nation[0]} nation={nation}/> 
                ))
              }
            </div>
            <div className={`${styles.bans} ${styles.action}`}>
              <p className="title">Баны:</p>
              {
                bans.map(nation => (
                  <HeadbookCiv5Item key={nation[0]} nation={nation}/> 
                ))
              }
            </div>
            <div className={`${styles.picks} ${styles.action}`}>
              <p className="title">Пики:</p>
            </div>
          </div>
          <div className={styles.nations}>
            {jsonData ? (
              <div className={`text ${styles.nation}`}>
                {          
                  Object.entries(jsonData).map(nation => {
                      let used = false
                      usedNations.forEach(el => {
                        if(el.toString() === nation.toString())
                        {
                          used = true
                        }
                      })
                      if (!used){
                        return(
                          nation[0].toLowerCase() ? (
                            <div className={styles.nation__wrapper}>
                              <HeadbookCiv5Item key={nation[0]} nation={nation}/> 
                              <div 
                              onClick={
                                () => {
                                  pick(nation)
                                  console.log(nation)
                              }} 
                              className={`${styles.nation__btn} ${startGame ? '' : styles.nation__btn_hidden}`}
                              >Выбрать</div>
                            </div>
                          ) : null
                        )
                      }
                      used = false
                  })
                }
              </div>
            ) : (
              <p className='text'>Идет загрузка наций...</p>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
