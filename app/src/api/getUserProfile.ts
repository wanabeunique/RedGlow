import axios from "axios";
import { toast } from "react-toastify";
import IProfile from "../interfaces/IProfile";

export default async function getUserProfile(username: string): Promise<IProfile> {
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user/${username}/info`,
    );
    return response.data;
  } catch (error) {
    toast.error('Ошибка загрузки профиля');
    return Promise.reject(error);
  }
}
