import axios from "axios";
import { setIsAuth } from "../store/reducers/isAuthSlice";
import Cookies from "js-cookie";
import { createAsyncThunk } from "@reduxjs/toolkit";


export const setLogout = createAsyncThunk<undefined, undefined, {rejectValue: string}>(
  'isAuth/logout',
  async function (_, { rejectWithValue }){
    try{
      axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')
      await axios.put(
        `${import.meta.env.VITE_API_SERVER}/user/session/`,
        {},
        {
          withCredentials: true,
        }
      ) 
    }
    catch(error){
      return rejectWithValue('Ошибка сервера')
    }   
  }
)