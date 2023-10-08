import axios from "axios";
import { toast } from "react-toastify";
import Cookies from "js-cookie";

export default async function getFriendsRequestOut(): Promise<Array<any>> {
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user/invite/out`,
    );
    console.log(response);
    return response.data;
  } catch (error) {
    toast.error("Ошибка получения исходящих запросов в друзья");
    console.log(error);
    throw error;
  }
}
