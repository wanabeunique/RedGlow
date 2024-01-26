import axios from 'axios';
import store from '@/store/store';
import { setPhoto, setUsername } from '../store/reducers/userSlice';
import { setIsAuth } from '../store/reducers/isAuthSlice';
import { toast } from 'react-toastify';
import connectSockets from '@/socket/connectSockets';
import ILogin from '@/interfaces/ILogin';
import IRegistration from '@/interfaces/IRegistration';
connectSockets();

class authSercive {
  private url = 'user';

  // Проверка авторизации пользователя
  getIsAuth = async () => {
    return await axios.get(`/${this.url}/checker`).then((res) => {
      if (res.status == 200) {
        store.dispatch(setUsername(res.data.username));
        store.dispatch(setIsAuth(true));
        store.dispatch(setPhoto(res.data.photo));
        connectSockets();
      }
    });
  };

  confirmRegistration = async (email: string, code: string) => {
    return await axios.put(`/users/`, {
      email,
      code,
    });
  };

  registration = async (data: IRegistration) => {
    return await axios
      .post(`${import.meta.env.VITE_API_SERVER}/users/`, data)
      .then(() => {
        toast.success('Потверждение регистрации было отправлено на почту');
      })
      .catch((e) => {
        if (e.response.status === 400) {
          for (var key in e.response.data) {
            toast.error(`${key}: ${e.response.data[key]}`);
          }
        } else if (e.response.status === 403) {
          toast.error('Вы уже авторизованы');
        } else {
          toast.error('Ошибка');
        }
      });
  };

  logout = async () => {
    return await axios.put(`/${this.url}/session/`).then(() => {
      store.dispatch(setPhoto(null));
      store.dispatch(setIsAuth(false));
    });
  };

  login = async (data: ILogin) => {
    return axios
      .post(`${this.url}/session/`, data)
      .then((response) => {
        store.dispatch(setIsAuth(true));
        store.dispatch(setUsername(response.data.username));
        store.dispatch(
          setPhoto(`${import.meta.env.VITE_API_SERVER}${response.data.photo}`),
        );
        toast.success('Вы успешно авторизировались');
        connectSockets();
      })
      .catch(() => {
        toast.error('Неправильный логин или пароль');
      });
  };
}

export default new authSercive();
