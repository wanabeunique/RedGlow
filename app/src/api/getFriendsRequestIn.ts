import axios from "axios";
import { toast } from "react-toastify";

export default async function getFriendsRequestIn(): Promise<Array<any>>{
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user/invite/in`,
    )
    return response.data;
  } catch (error) {
      toast.error('Ошибка получения входящих запросов в друзья');
      console.log(error)
      throw error;
  }
}
