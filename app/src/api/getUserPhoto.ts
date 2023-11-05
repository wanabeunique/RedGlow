import axios from "axios";
import { toast } from "react-toastify";

export default async function getUserPhoto(username: string): Promise<string>{
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user/${username}/photo`,
    )
    return response.data.photo;
  } catch (error) {
      toast.error('Ошибка при получении фото');
      console.log(error)
      throw error;
  }
}
