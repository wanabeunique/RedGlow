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
      {withCredentials: true, headers:{"X-CSRFTOKEN":Cookies.get('csrftoken')}}
    )
    toast.success(`Запрос пользователю ${data.accepter} отправлен`)
  } catch (error) {
    toast.error('Ошибка в запросе')
  }
}
