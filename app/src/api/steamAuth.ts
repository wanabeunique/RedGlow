import axios from "axios";
import { setIsAuth } from "../store/reducers/isAuthSlice";
import { setUsername } from "../store/reducers/userSlice";
import { toast } from "react-toastify";
import connectSockets from "../socket/connectSockets";
import ILogin from "../interfaces/ILogin";

export default async function login(data: ILogin, dispatch: any) {
  axios
    .post(`http://api.steampowered.com/ISteamUser/<название метода>/v<версия>/?key=<ключ api>&format=<формат>.`, data, {
    })
    .then((response) => {
      dispatch(setIsAuth(true));
      dispatch(setUsername(response.data.username));
      toast.success("Вы успешно авторизировались");
      connectSockets();
      return response.status;
    })
    .catch (function (err) {
      toast.error('Неправильный логин или пароль')
    })
}


