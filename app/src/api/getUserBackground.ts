import axios from 'axios';
import { toast } from 'react-toastify';

export default async function getUserBackground(
  username: string,
): Promise<string> {
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user/${username}/background`,
    );
    return response.data.background;
  } catch (error) {
    toast.error('Ошибка при получении заднего фона');
    console.log(error);
    throw error;
  }
}
