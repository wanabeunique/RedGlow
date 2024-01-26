import { useState } from 'react';
import { ToastContainer } from 'react-toastify';
import Footer from '@/components//Footer/Footer';
import Preloader from '@/components/Preloader';
import Paths from './components/Paths/Paths';
import './axiosInterceptor' 
import authService from './service/auth.service';

function App() {
  const [isLoading, setIsLoading] = useState(false);

  const isDarktheme = document
    .querySelector('html')
    ?.classList.contains('dark');

  authService.getIsAuth() 

  return (
    <>
      {isLoading ? (
        <div className="w-screen h-screen flex justify-center items-center">
          <Preloader />
        </div>
      ) : (
        <>
          <Paths />
          <ToastContainer theme={isDarktheme ? 'dark' : 'light'} />
          <Footer />
        </>
      )}
    </>
  );
}

export default App;
