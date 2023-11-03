import { useEffect } from 'react'
import ProfileSettings from './pages/Profile/ProfileSettings'
import Cookies from 'js-cookie'
import getIsAuth from './api/getIsAuth'
import connectSockets from './socket/connectSockets'
import { useAppSelector } from './hooks'
import axios, { AxiosHeaders } from 'axios'
import { Routes, Route} from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import Footer from './pages/Footer/Footer'
import Headbook from './pages/Headbook/Headbook'
import Layout from './pages/Layout/Layout'
import Homepage from './pages/Homepage/Homepage'
import Login from './pages/Login/Login'
import Registration from './pages/Registration/Registration'
import NotFound from './pages/NotFound/NotFound'
import Profile from './pages/Profile/Profile'
import EmailConfirm from './pages/EmailConfirm/EmailConfirm'
import Generate from './pages/Genarate/Generate'
import Recovery from './pages/Recovery/Recovery'
import Steam from './pages/Steam/Steam'
import RecoveryNewPassword from './pages/Recovery/RecoveryNewPassword'

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
  
  const isAuth = useAppSelector((state) => state.authReducer.data)
  const dispatch = useAppSelector

  useEffect(() => {
    getIsAuth()
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
            <Route path='/headbook/*' element={<Headbook/>} />
            <Route path='/login' element={<Login />}></Route>
            <Route path='/registration' element={<Registration />}></Route>
            <Route path='/profile/:searchName' element={<Profile />}></Route>
            <Route path='/generate' element={<Generate />}></Route>   
            <Route path='/recovery'element={<Recovery />}/>   
            <Route path='/steam' element={<Steam />}/>
            <Route path='/settings' element={<ProfileSettings />} />
            <Route path='/forgot/password/' element={<RecoveryNewPassword />}></Route>
            <Route path='/404' element={<NotFound/>}></Route>
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
