import { setPhoto } from "@/store/reducers/userSlice";
import store from "@/store/store";
import axios from "axios";
import { toast } from "react-toastify";

export default async function changePhoto(file: any): Promise<Array<any>>{
  console.log((file))
  const formData = new FormData()
  formData.append('photo', file)
  try {
    const response = await axios.put(
      `${import.meta.env.VITE_API_SERVER}/user/photo/`,
      formData
    )
    toast.success('Вы успешно сменили фото');
    store.dispatch(setPhoto(response.data.photo))
    return response.data;
  } catch (error) {
      toast.error('Ошибка при смене фото');
      console.log(error)
      throw error;
  }
}
