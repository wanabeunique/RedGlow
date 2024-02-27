import { useState } from 'react';
import { ToastContainer } from 'react-toastify';
import Footer from '@/components//Footer/Footer';
import Preloader from '@/components/Preloader';
import Paths from './components/Paths/Paths';
import './axiosInterceptor';
import authService from './service/auth.service';
import { useTheme } from './components/ui/theme-provider';
import Search from './components/Play/Search';
import GameAccept from './components/Play/GameAccept';
import { useAppSelector } from './hooks/useAppSelector';
import { useColorSheme } from './hooks/useColorSheme';

function App() {
  const searchActive = useAppSelector(
    (state) => state.gameReducer.activeSearch,
  );
  const acceptActive = useAppSelector(
    (state) => state.gameAcceptReducer.isActive,
  );
  console.log(acceptActive)

  const [isLoading, setIsLoading] = useState(false);

  const { theme } = useTheme();
  useColorSheme()

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
          {acceptActive && <GameAccept />}
          {searchActive && <Search />}
          <Footer />
        </>
      )}
    </>
  );
}

export default App;
