import axios from "axios";
import { toast } from "react-toastify";


export default async function getRecoveryPasswordLink(email: String){
  try{
    const response = await axios.post(
      `${import.meta.env.VITE_API_SERVER}/user/help/link/`,
      {
        "email": email
      },
    )
    if (response.status == 202){
      toast.success('Письмо успешно отправлено на почту')
      return response.status
    }
  }
  catch(e: unknown){
    e.response.data.errors.forEach((error: string) => {
      toast.error(error)
    });
  }
}
