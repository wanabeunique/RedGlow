import axios from "axios";
import { setIsAuth } from "../store/reducers/isAuthSlice";
import Cookies from "js-cookie";

export default async function getIsAuth(dispatch){
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')
  try{
    const response = await axios.put(
      'api/user/checker/',
      {withCredentials: true}
    )
    if (response.status == 200){
      dispatch(setIsAuth(true))
    }
  }
  catch(error){
    console.log(error)
    dispatch(setIsAuth(false))
  }
}