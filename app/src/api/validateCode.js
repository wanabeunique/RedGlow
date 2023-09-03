import axios from "axios";
export default async function validateCode(data){
  try {
    console.log(data)
    const response = await axios.put(`http://127.0.0.1:8000/users/confirm/`, data)
    return response
  } catch (error) {
    return error.response
  }
}