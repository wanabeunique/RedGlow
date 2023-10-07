import axios from "axios";
import Cookies from "js-cookie";

export default async function validateCode(code: string, key: string) {
  const data = {
    code: code,
    key: key,
  }
  console.log(data)
  try {
    const response = await axios.put(
      `${import.meta.env.VITE_API_SERVER}/users/`,
      data,
      {
        withCredentials: true,
        headers: { "X-CSRFTOKEN": Cookies.get("csrftoken") },
      }
    );
    return response;
  } catch (error: any) {
    return error.response;
  }
}
