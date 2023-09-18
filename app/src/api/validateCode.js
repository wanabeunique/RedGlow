import axios from "axios";
export default async function validateCode(data){
  try {
    console.log(data)
    const response = await axios.put(
      `${import.meta.env.VITE_API_SERVER}/users/`, 
      data)
    return response
  } catch (error) {
    return error.response
  }
}