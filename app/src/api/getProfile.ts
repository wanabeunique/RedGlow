import axios from "axios";
import { toast } from "react-toastify";
import { IOwnProfile } from "@/interfaces/IOwnProfile";

export default async function getProfile(): Promise<IOwnProfile> {
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user/info`,
    );
    return response.data;
  } catch (error) {
    toast.error('Ошибка загрузки профиля');
    return Promise.reject(error);
  }
}
