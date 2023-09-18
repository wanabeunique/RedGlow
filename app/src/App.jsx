import './App.sass'

import { useEffect } from 'react'
import { Routes, Route} from 'react-router-dom'
import { useDispatch } from 'react-redux'
import { ToastContainer } from 'react-toastify'

import Footer from './components/Footer/Footer'
import Headbook from './components/Headbook/Headbook'
import Layout from './components/Layout/Layout'
import Homepage from './components/Homepage/Homepage'
import Login from './components/Login/Login'
import Registration from './components/Registration/Registration'
import NotFound from './components/NotFound/NotFound'
import Profile from './components/Profile/Profile'
import Friends from './components/Friends/Friends'
import EmailConfirm from './components/EmailConfirm/EmailConfirm'
import Generate from './components/Genarate/Generate'
import Recovery from './components/Recovery/Recovery'
import getIsAuth from './api/getIsAuth'
import connectSockets from './socket/connectSockets'
import { useSelector } from 'react-redux'



function App() {
  const isAuth = useSelector((state) => state.authReducer.data)
  const dispatch = useDispatch()
  useEffect(() => {
    getIsAuth(dispatch)
  }, [])
  useEffect(() => {
    if (isAuth){
      connectSockets()
    }
  }, [isAuth])
  return (
    <>
        <Routes>
            <Route path='/' element={<Layout/>}>
            <Route path='/signUp/confirm' element={<EmailConfirm />}/>
            <Route path='*' element={<NotFound />}></Route>
            <Route index element={<Homepage />} />
            <Route path='/Headbook/*' element={<Headbook/>} />
            <Route path='/Login' element={<Login />}></Route>
            <Route path='/Registration' element={<Registration />}></Route>
            <Route path='/Profile' element={<Profile />}></Route>
            <Route path='/Friends' element={<Friends />}></Route>
            <Route path='/Generate' element={<Generate />}></Route>   
            <Route path='/Recovery'element={<Recovery />}/>   
          </Route>
        </Routes>
      <ToastContainer />
      <Footer />
    </>
  )
}

export default App
