import axios from "axios";

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
    );
    return response;
  } catch (error: any) {
    return error.response;
  }
}
