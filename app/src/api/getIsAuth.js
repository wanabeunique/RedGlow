import axios from "axios";
import { setIsAuth } from "../store/reducers/isAuthSlice";
import { setUsername } from "../store/reducers/userSlice";
import Cookies from "js-cookie";

export default async function getIsAuth(dispatch){
  axios.defaults.headers.common['csrftoken'] = Cookies.get('csrftoken')
  try{
    const response = await axios.put(
      `${import.meta.env.VITE_API_SERVER}/user/checker/`,
      {},
      {withCredentials: true,headers:{"X-CSRFTOKEN":Cookies.get('csrftoken')}}
    )
    if (response.status == 202){
      dispatch(setUsername(response.data.username))
      dispatch(setIsAuth(true))
    }
    console.log(response)
  }
  catch(error){
    console.log(Cookies.get('csrftoken'))
    console.log(error)
    dispatch(setIsAuth(false))
  }
}