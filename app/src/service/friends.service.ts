import axios from 'axios';
import { toast } from 'react-toastify';
import store from '@/store/store';
import {
  removeFriendIn,
  removeFriendCurrent,
} from '@/store/reducers/friendsSlice';

class friendsService {
  private url = 'user';

  //Все друзья пользователя
  getUserFriends = async (targetName: string, page: number) => {
    return await axios
      .get(`${this.url}/${targetName}/friend/page/${page}`)
      .then((res) => {
        return res.data;
      });
  };

  //Входящие заявки в друзья
  getRequestInByPage = async (page: number) => {
    return await axios.get(`${this.url}/invite/in/page/${page}`).then((res) => {
      return res.data;
    });
  };

  //Исходящие заявки в друзья
  getRequestOutByPage = async (page: number) => {
    return await axios
      .get(`${this.url}/invite/out/page/${page}`)
      .then((res) => {
        return res.data;
      });
  };

  //Поиск по значению и странице
  searchUsers = async (value: string, page: number) => {
    return await axios
      .get(`${this.url}/prefix/${value}/page/${page}`)
      .then((res) => {
        return res.data;
      })
      .catch(() => {
        return [];
      });
  };

  // Удаление друга по никнейму
  removeFriend = async (nickname: string) => {
    const data = { accepter: nickname.trim() };
    return await axios.put(`${this.url}/friend/`, data).then((res) => {
      if (res.status == 200) {
        toast.success(`Вы отметили заявку ${data.accepter}`);
        store.dispatch(removeFriendIn(nickname));
      } else if (res.status == 202) {
        toast.success(`Вы удалили из друзей ${data.accepter}`);
        store.dispatch(removeFriendCurrent(nickname));
      }
      return { status: res.status, nickname: data.accepter };
    });
  };

  // Добавление друга по никнейму
  addfriend = async (nickname: string) => {
    const data = { accepter: nickname.trim() };
    return await axios
      .post(`${this.url}/friend/`, data)
      .then((res) => {
        if (res.status == 201) {
          toast.success(`Запрос пользователю ${data.accepter} отправлен`);
        } else if (res.status == 202) {
          toast.success(`Вы успешно добавили ${data.accepter}`);
        }
        return { status: res.status, nickname: data.accepter };
      })
      .catch(() => {
        toast.error('Ошибка в запросе');
      });
  };
}

export default new friendsService();
