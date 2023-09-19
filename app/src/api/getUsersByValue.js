import axios from "axios";
import { toast } from "react-toastify";
import Cookies from "js-cookie";

export default async function getUsersByValue(value) {
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/users/prefix/${value}/`,
      {withCredentials: true,headers:{"X-CSRFTOKEN":Cookies.get('csrftoken')}}
    )
    return response;
  } catch (error) {
      toast.error('Ошибка получения пользователей');
      console.log(error)
    throw error;
  }
}
