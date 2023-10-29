import axios from "axios";
import { toast } from "react-toastify";
import { IOwnProfile } from "@/interfaces/IOwnProfile";

export default async function setSteam(steamId: any): Promise<IOwnProfile> {
  const data = {
    steamId: steamId
  }
  try {
    const response = await axios.put(
      `${import.meta.env.VITE_API_SERVER}/user/steamId/`,
      data
    );
    toast.success('Стим успешно привязан')
    return response.data;
  } catch (error) {
      console.log(error)
      toast.error('Ошибка привязки Steam');
      return Promise.reject(error);
  }
}
