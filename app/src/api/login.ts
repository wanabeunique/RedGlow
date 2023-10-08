import axios from "axios";
import { setIsAuth } from "../store/reducers/isAuthSlice";
import { setUsername } from "../store/reducers/userSlice";
import { toast } from "react-toastify";
import connectSockets from "../socket/connectSockets";
import ILogin from "../interfaces/ILogin";
import { Console } from "console";

export default async function login(data: ILogin, dispatch: any) {
  try {
    axios
      .post(`${import.meta.env.VITE_API_SERVER}/user/session/`, data, {
      })
      .then((response) => {
        dispatch(setIsAuth(true));
        dispatch(setUsername(response.data.username));
        toast.success("Вы успешно авторизировались");
        connectSockets();
        return response.status;
      });
  } catch (error) {
    throw error;
  }
}
