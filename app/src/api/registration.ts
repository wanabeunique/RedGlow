import axios from "axios";
import { toast } from "react-toastify";
import IRegistration from "../interfaces/IRegistration";

export default async function registrationSubmit(data: IRegistration) {
  try {
    const response = await axios.post(
      `${import.meta.env.VITE_API_SERVER}/users/`,
      data);
    toast.success('Потверждение регистрации было отправлено на почту');
    return response; // Возвращаем объект ответа
  } catch (error: any) {
    if (error.response.status === 400) {
      for(var key in error.response.data){
        toast.error(`${key}: ${error.response.data[key]}`)
      }
    } else if (error.response.status === 403) {
      toast.error('Вы уже авторизованы');
    } else {
      toast.error('Ошибка');
    }
    throw error;
  }
}
