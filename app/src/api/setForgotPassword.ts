import axios from 'axios';
import { toast } from 'react-toastify';

export default async function setForgotPassword(
  password: String,
  email: String,
  code: String,
) {
  try {
    const response = await axios.put(
      `${import.meta.env.VITE_API_SERVER}/user/help/password/`,
      {
        password: password,
        email: email,
        code: code,
      },
    );
    if (response.status == 200) {
      toast.success('Вы успешно сменили пароль');
      return response.status;
    }
  } catch (e: unknown) {
    e.response.data.errors.forEach((error: string) => {
      toast.error(error);
    });
  }
}
