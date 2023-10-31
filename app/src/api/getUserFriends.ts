import axios from "axios";
import Cookies from "js-cookie";

export default async function getUserFriends(targetName: string, page: number): Promise<any> {
  axios.defaults.headers.common["csrftoken"] = Cookies.get("csrftoken");
  try { const res = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/user/${targetName}/friend/page/${page}`
    );
    return res.data;
  } catch (error) {
    console.log(error);
  }
}
