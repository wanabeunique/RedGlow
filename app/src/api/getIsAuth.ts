import axios from "axios"; import { setIsAuth } from "../store/reducers/isAuthSlice";
import { setPhoto, setUsername } from "../store/reducers/userSlice";
import Cookies from "js-cookie";
import store from "@/store/store";

export default async function getIsAuth(){
  axios.defaults.headers.common['csrftoken'] = Cookies.get('csrftoken')
  try{
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user/checker/`,
    )
    if (response.status == 200){
      store.dispatch(setUsername(response.data.username))
      store.dispatch(setIsAuth(true))
      store.dispatch(setPhoto(response.data.photo))
    }
  }
  catch(error){
    console.log(Cookies.get('csrftoken'))
    console.log(error)
    store.dispatch(setIsAuth(false))
  }
}
