import axios from "axios"
import Cookies from "js-cookie"

export default async function getUserFriends(targetName: string): Promise<any> {
  axios.defaults.headers.common['csrftoken'] = Cookies.get('csrftoken')
  console.log(`${import.meta.env.VITE_API_SERVER}/user/${targetName}/friend`)
  return await axios.get(
    `${import.meta.env.VITE_API_SERVER}/user/${targetName}/friend`,
  )
  .then(res => {res.data; console.log(res)})
  .catch(error  => {error.response.data.message; console.log(error)})
}