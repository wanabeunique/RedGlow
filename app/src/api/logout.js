import axios from "axios";
import { setIsAuth } from "../store/reducers/isAuthSlice";
import Cookies from "js-cookie";


export default async function logout(dispatch){
  console.log(Cookies.get('csrftoken'))
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')
  const response = await axios.put(
    'api/user/session/',
    {},
    {
      withCredentials: true,
    }
  )
  console.log(response)
  if (response.status == 200){
    console.log(response.status)
    dispatch(setIsAuth(false))
    console.log(response)
    return response.status
  }
}