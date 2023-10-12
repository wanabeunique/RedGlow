import { useEffect } from 'react'
import { Routes, Route} from 'react-router-dom'
import { useDispatch } from 'react-redux'
import { ToastContainer } from 'react-toastify'

import Footer from './pages/Footer/Footer'
import Headbook from './pages/Headbook/Headbook'
import Layout from './pages/Layout/Layout'
import Homepage from './pages/Homepage/Homepage'
import Login from './pages/Login/Login'
import Registration from './pages/Registration/Registration'
import NotFound from './pages/NotFound/NotFound'
import Profile from './pages/Profile/Profile'
import Friends from './pages/Friends/Friends'
import EmailConfirm from './pages/EmailConfirm/EmailConfirm'
import Generate from './pages/Genarate/Generate'
import Recovery from './pages/Recovery/Recovery'
import getIsAuth from './api/getIsAuth'
import connectSockets from './socket/connectSockets'
import { useAppSelector } from './hooks'
import axios, { AxiosHeaders } from 'axios'
import Cookies from 'js-cookie'
import Steam from './pages/Steam/Steam'

axios.interceptors.request.use(
  function(config) {
    config.withCredentials = true
    const newConfig = Object.assign({}, config, {
      headers: {
        ...(config.headers) as AxiosHeaders,
        'X-CSRFTOKEN': Cookies.get('csrftoken')
      },
  });
  return newConfig;
  },
  function(error) {
    return Promise.reject(error);
  }
);

function App() {
  const isDarktheme = document.querySelector('html')?.classList.contains('dark')
  console.log(isDarktheme)

  const isAuth = useAppSelector((state) => state.authReducer.data)
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
            {/* <Route path='/Friends' element={<Friends />}></Route> */}
            <Route path='/Generate' element={<Generate />}></Route>   
            <Route path='/Recovery'element={<Recovery />}/>   
            <Route path='/Steam' element={<Steam />}/>
          </Route>
        </Routes>
      <ToastContainer 
        theme={isDarktheme ? 'dark' : 'light'}
      />
      <Footer />
    </>
  )
}

export default App
