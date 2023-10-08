import axios from "axios";
import Cookies from "js-cookie";
import { toast } from "react-toastify";


export default async function recoveryPassword(email: string){
  console.log(Cookies.get('csrftoken'))
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')
  try{
    const response = await axios.post(
      `${import.meta.env.VITE_API_SERVER}/user/help/link/`,
      {
        "email": email
      },
    )
    if (response.status == 200){
      toast.success('Письмо успешно отправлено на почту')
      return response.status
    }
  }
  catch(e){
    console.log(e)
    toast.error('Ошибка при отправке письма')
  }
}