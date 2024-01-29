import { useState } from 'react';
import { ToastContainer } from 'react-toastify';
import Footer from '@/components//Footer/Footer';
import Preloader from '@/components/Preloader';
import Paths from './components/Paths/Paths';
import './axiosInterceptor';
import authService from './service/auth.service';
import { useTheme } from './components/ui/theme-provider';

function App() {
  const [isLoading, setIsLoading] = useState(false);

  const { theme } = useTheme();

  authService.getIsAuth();

  return (
    <>
      {isLoading ? (
        <div className="w-screen h-screen flex justify-center items-center">
          <Preloader />
        </div>
      ) : (
        <>
          <Paths />
          <ToastContainer theme={theme} />
          <Footer />
        </>
      )}
    </>
  );
}

export default App;
