import axios from "axios";
import { toast } from "react-toastify";
import Cookies from "js-cookie";
import IProfile from "../interfaces/IProfile";

export default async function getProfile(): Promise<IProfile> {
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user`,
      { withCredentials: true, headers: { "X-CSRFTOKEN": Cookies.get('csrftoken') } }
    );
    return response.data;
  } catch (error) {
    toast.error('Ошибка загрузки профиля');
    return Promise.reject(error);
  }
}
