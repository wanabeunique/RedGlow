import axios from "axios";
import { setIsAuth } from "../store/reducers/isAuthSlice";


export default async function login(data, dispatch){
  axios.post(
    `${import.meta.env.VITE_API_SERVER}/user/session/`,
    data,
    {withCredentials: true}
  )
  .then( (response) => {
    dispatch(setIsAuth(true))
    console.log(response)
    return response.status
  })
}