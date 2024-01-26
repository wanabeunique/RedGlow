import { Routes, Route } from 'react-router-dom';
import ProfileSettings from '@/pages/Profile/ProfileSettings';
import Layout from '@/layouts/Layout/Layout';
import Homepage from '@/pages/Homepage/Homepage';
import Login from '@/pages/Login/Login';
import Registration from '@/pages/Registration/Registration';
import NotFound from '@/pages/NotFound/NotFound';
import Profile from '@/pages/Profile/Profile';
import EmailConfirm from '@/pages/EmailConfirm/EmailConfirm';
import Recovery from '@/pages/Recovery/Recovery';
import Steam from '@/pages/Steam/Steam';
import RecoveryNewPassword from '@/pages/Recovery/RecoveryNewPassword';
import PrivateRoute from '../PrivateRoute/PrivateRoute';
import { useAppSelector } from '@/hooks/useAppSelector';

export default function Paths(){
  const isAuth = useAppSelector((state) => state.authReducer.data)

  console.log('Пользователь авторизован' + isAuth)
  
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route path="/signUp/confirm" element={<EmailConfirm />} />
        <Route path="*" element={<NotFound />}></Route>
        <Route index element={<Homepage />} />
        <Route path="/login" element={<Login />}></Route>
        <Route path="/registration" element={<Registration />}></Route>
        <Route path="/profile/:searchName" element={<Profile />}></Route>
        <Route path="/recovery" element={<Recovery />} />
        <Route path="/steam" element={<Steam />} />
        <Route path="/settings" element={<PrivateRoute isAuth={isAuth}><ProfileSettings /></PrivateRoute>} />
        <Route path="/forgot/password/" element={<RecoveryNewPassword />}></Route>
        <Route path="/404" element={<NotFound />}></Route>
      </Route>
    </Routes>     
  )
}

