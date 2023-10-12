import axios from "axios";
import { toast } from "react-toastify";

export default async function changePassword(currentPassword: string,newPassword: string): Promise<Array<any>>{
  const data = {
    "currentPassword": currentPassword,
    "newPassword": newPassword
  }
  try {
    const response = await axios.put(
      `${import.meta.env.VITE_API_SERVER}/user/password/`,
      data
    )
    console.log(response)
    toast.success('Вы успешно сменили  пароль');
    return response.data;
  } catch (error) {
      toast.error('Ошибка при смене пароля');
      console.log(error)
      throw error;
  }
}
