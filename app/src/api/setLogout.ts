import axios from "axios";
import Cookies from "js-cookie";
import store from "@/store/store";
import { setPhoto } from "@/store/reducers/userSlice";
import { setIsAuth } from "@/store/reducers/isAuthSlice";

export default async function setLogout(){
  try{
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')
    await axios.put(
      `${import.meta.env.VITE_API_SERVER}/user/session/`,
      {},
    )
    store.dispatch(setPhoto(undefined))
    store.dispatch(setIsAuth(false))
  }
  catch(error){
    console.log(error)
  }   
}

