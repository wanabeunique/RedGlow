import axios from "axios";
import { setIsAuth } from "../store/reducers/isAuthSlice";
import { setUsername } from "../store/reducers/userSlice";
import Cookies from "js-cookie";

export default async function getIsAuth(dispatch: any){
  axios.defaults.headers.common['csrftoken'] = Cookies.get('csrftoken')
  try{
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user/checker/`,
    )
    if (response.status == 200){
      dispatch(setUsername(response.data.username))
      dispatch(setIsAuth(true))
    }
  }
  catch(error){
    console.log(Cookies.get('csrftoken'))
    console.log(error)
    dispatch(setIsAuth(false))
  }
}