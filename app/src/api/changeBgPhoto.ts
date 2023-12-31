import axios from "axios";
import { toast } from "react-toastify";

export default async function changeBgPhoto(file: any): Promise<Array<any>>{
  console.log((file))
  const formData = new FormData()
  formData.append('background', file)
  try {
    const response = await axios.put(
      `${import.meta.env.VITE_API_SERVER}/user/background/`,
      formData
    )
    toast.success('Вы успешно сменили фото');
    return response.data;
  } catch (error) {
      toast.error('Ошибка при смене фото');
      console.log(error)
      throw error;
  }
}
