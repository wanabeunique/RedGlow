import axios from "axios"
import Cookies from "js-cookie"
import { toast } from "react-toastify"

export default async function sendFriendRequest(nickname) {
  nickname.trim()
  const data = {"accepter": nickname}
  console.log(data)
  console.log(nickname)
  console.log(typeof(nickname))
  axios.defaults.headers.common['csrftoken'] = Cookies.get('csrftoken')
  try {
    const response = await axios.post(
      `${import.meta.env.VITE_API_SERVER}/user/friend/`,
      data,
      {withCredentials: true, headers:{"X-CSRFTOKEN":Cookies.get('csrftoken')}}
    )
    console.log(response)
    toast.success('Запрос успешно отправлен')
  } catch (error) {
    console.log(error)
    toast.error('Ошибка в запросе')
  }
}
