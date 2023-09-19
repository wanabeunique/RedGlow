import axios from "axios";
import { toast } from "react-toastify";
import Cookies from "js-cookie";

export default async function getProfile() {
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user`,
      {withCredentials: true,headers:{"X-CSRFTOKEN":Cookies.get('csrftoken')}}
    )
    return response;
  } catch (error) {
      toast.error('Ошибка загрузки профиля');
    throw error;
  }
}
