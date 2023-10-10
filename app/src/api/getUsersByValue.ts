import axios from "axios";

export default async function getUsersByValue(value: string, page: number): Promise<Array<string>>{
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user/prefix/${value}/page/${page}`,
    ) 
    return response.data;
  } catch (error) {
      return []
  }
}
