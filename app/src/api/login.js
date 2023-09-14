import axios from "axios";
import { setIsAuth } from "../store/reducers/isAuthSlice";
import { setUsername } from "../store/reducers/userSlice";
import { toast } from "react-toastify";

export default async function login(data, dispatch){
  axios.post(
    `${import.meta.env.VITE_API_SERVER}/user/session/`,
    data,
    {withCredentials: true}
  )
  .then( (response) => {
    dispatch(setIsAuth(true))
    dispatch(setUsername(response.data.username))
    console.log(response)
    toast.success('Вы успешно авторизировались')
    return response.status
  })
}