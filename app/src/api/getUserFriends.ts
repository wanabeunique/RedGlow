import axios from "axios"
import Cookies from "js-cookie"

export default async function getUserFriends(targetName: string): Promise<any> {
  axios.defaults.headers.common['csrftoken'] = Cookies.get('csrftoken')
  return await axios.get(
    `${import.meta.env.VITE_API_SERVER}/user/${targetName}/friend`,
    {withCredentials: true,headers:{"X-CSRFTOKEN":Cookies.get('csrftoken')}}
  )
  .then(res => res.data)
  .catch(error  => {error.response.data.message; console.log(error)})
}