import axios from "axios";
import { toast } from "react-toastify";
import Cookies from "js-cookie";

export default async function getUsersByValue(value: string): Promise<Array<string>>{
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user/prefix/${value}/`,
    )
    
    return response.data;
  } catch (error) {
      toast.error('Ошибка получения пользователей');
      console.log(error)
      throw error;
  }
}
