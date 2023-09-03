import axios from "axios";
import { setIsAuth } from "../store/reducers/isAuthSlice";


export default async function login(data, dispatch){
  axios.post(
    'api/user/session/',
    data,
    {withCredentials: true}
  )
  .then( (response) => {
    dispatch(setIsAuth(true))
    console.log(response)
    return response.status
  })
}