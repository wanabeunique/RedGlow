import axios from "axios";
import Cookies from "js-cookie";

export default async function getUserFriends(targetName: string): Promise<any> {
  axios.defaults.headers.common["csrftoken"] = Cookies.get("csrftoken");
  console.log(`${import.meta.env.VITE_API_SERVER}/user/${targetName}/friend`);
  try {
    const res = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user/${targetName}/friend`
    );
    console.log(res)
    return res.data;
  } catch (error) {
    console.log(error);
  }
}
