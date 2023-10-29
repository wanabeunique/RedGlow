import axios from "axios";
import { setIsAuth } from "../store/reducers/isAuthSlice";
import { setPhoto, setUsername } from "../store/reducers/userSlice";
import { toast } from "react-toastify";
import connectSockets from "../socket/connectSockets";
import ILogin from "../interfaces/ILogin";

export default async function login(data: ILogin, dispatch: any) {
  axios
    .post(`${import.meta.env.VITE_API_SERVER}/user/session/`, data, {
    })
    .then((response) => {
      dispatch(setIsAuth(true));
      dispatch(setUsername(response.data.username));
      dispatch(setPhoto(response.data.photo))
      toast.success("Вы успешно авторизировались");
      connectSockets();
      return response.status;
    })
    .catch (function (err) {
      toast.error('Неправильный логин или пароль')
    })
}
