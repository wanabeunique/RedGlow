import axios from "axios"
import { toast } from "react-toastify"

export default async function removeFriend(nickname:  string) {
  const data = {"accepter": nickname.trim()}
  console.log(data)
  try {
    const response = await axios.put(
      `${import.meta.env.VITE_API_SERVER}/user/friend/`,
      data,
    )
    if (response.status == 200){
      toast.success(`Вы отметили заявку ${data.accepter}`)
    }
    else if (response.status == 202){
      toast.success(`Вы удалили из друзей ${data.accepter}`)
    }
    return {status: response.status, nickname: data.accepter} 
  } catch (error) {
    console.log(error)
    toast.error('Ошибка в запросе')
  }
}
