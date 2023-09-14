import axios from "axios"
import Cookies from "js-cookie"

export default async function getUserFriends(targetName){
  console.log(targetName)
  console.log(`${import.meta.env.VITE_API_SERVER}`, `/${targetName}`, `/friend`)
  axios.defaults.headers.common['csrftoken'] = Cookies.get('csrftoken')
  try{
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user/${targetName}/friend`,
      {withCredentials: true,headers:{"X-CSRFTOKEN":Cookies.get('csrftoken')}}
    )
    console.log(response)
    return response
  }
  catch(error){
    console.log(error)
  }
}