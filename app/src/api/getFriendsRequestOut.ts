import axios from "axios";
import { toast } from "react-toastify";

export default async function getFriendsRequestOut(page: number): Promise<Array<any>> {
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user/invite/out/page/${page}`,
    );
    return response.data;
  } catch (error) {
    toast.error("Ошибка получения исходящих запросов в друзья");
    console.log(error);
    throw error;
  }
}
