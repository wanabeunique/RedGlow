import axios from 'axios';
import { toast } from 'react-toastify';

class passwordService {
  sendPasswordResetLink = async (email: string) => {
    return await axios
      .post(`user/help/link/`, {
        email,
      })
      .then((res) => {
        if (res.status === 200) {
          toast.success('Письмо успешно отправлено на почту');
          return res.status;
        }
      })
      .catch(() => {
        toast.error('Ошибка при отправке письма');
      });
  };

  checkEmailCode = async (email: string, code: string) => {
    return axios.get(`email/${email}/code/${code}`).then(() => {
      return true;
    }); // TODO: Если я не исправлю это до 28.01.2024 я оторву себе руки
  };

  setForgottenPassword = async (
    password: string,
    email: string,
    code: string,
  ) => {
    return await axios
      .put(`user/help/password/`, {
        password: password,
        email: email,
        code: code,
      })
      .then((res) => {
        if (res.status) {
          toast.success('Вы успешно сменили пароль');
          return res.status;
        }
      });
  };

  changePassword = async (currentPassword: string, newPassword: string) => {
    return await axios
      .put(`/user/password/`, {
        currentPassword,
        newPassword,
      })
      .then((res) => {
        toast.success('Вы успешно сменили  пароль');
        return res.data;
      })
      .catch(() => {
        toast.error('Ошибка при смене пароля');
      });
  };
}

export default new passwordService();
