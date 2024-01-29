import axios from 'axios';
import { toast } from 'react-toastify';
import store from '@/store/store';
import { setPhoto } from '@/store/reducers/userSlice';

class userService {
  private url = 'user';

  getProfile = async () => {
    return await axios.get(`${this.url}/info`).then((res) => {
      return res.data;
    });
  };

  getUserProfile = async (username: string) => {
    return await axios.get(`${this.url}/${username}/info`).then((res) => {
      return res.data;
    });
  };

  getUserBackground = async (username: string) => {
    return await axios.get(`${this.url}/${username}/background`).then((res) => {
      return res.data.background;
    });
  };

  linkSteamAccount = async (steamId: string) => {
    return await axios
      .put(`${this.url}/steamId/`, { steamId })
      .then((res) => {
        toast.success('Стим успешно привязан');
        return res.data;
      })
      .catch(() => {
        toast.error('Ошибка привязки Steam');
      });
  };

  getUserPhoto = async (username: string) => {
    return await axios.get(`${this.url}/${username}/photo`).then((res) => {
      return res.data.photo;
    });
  };

  setUserPhoto = async (file: any) => {
    const formData = new FormData();
    formData.append('photo', file);
    return await axios
      .put(`${this.url}/photo/`, formData)
      .then((res) => {
        toast.success('Вы успешно сменили фото');
        store.dispatch(setPhoto(res.data.photo));
        return res.data;
      })
      .catch(() => {
        toast.error('Ошибка при смене фото');
      });
  };

  setBgPhoto = async (file: any) => {
    const formData = new FormData();
    formData.append('background', file);
    return await axios
      .put(`${this.url}/background/`, formData)
      .then((res) => {
        toast.success('Вы успешно сменили фото');
        return res.data;
      })
      .catch(() => {
        toast.error('Ошибка при смене фото');
      });
  };
}

export default new userService();
