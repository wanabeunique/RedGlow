import axios from "axios"
import Cookies from "js-cookie"
import { toast } from "react-toastify"

export default async function sendFriendRequest(nickname:  string) {
  const data = {"accepter": nickname.trim()}
  axios.defaults.headers.common['csrftoken'] = Cookies.get('csrftoken')
  try {
    const response = await axios.post(
      `${import.meta.env.VITE_API_SERVER}/user/friend/`,
      data,
    )
    if (response.status == 201){
      toast.success(`Запрос пользователю ${data.accepter} отправлен`)
    }
    else if (response.status == 202){
      toast.success(`Вы успешно добавили ${data.accepter}`)
    }
    return {status: response.status, nickname: data.accepter}
  } catch (error) {
    toast.error('Ошибка в запросе')
  }
}
