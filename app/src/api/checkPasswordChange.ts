import axios from 'axios';

export default async function checkPasswordChange(
  email: string,
  code: string,
): Promise<boolean> {
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_SERVER}/email/${email}/code/${code}`,
    );
    return true;
  } catch (error) {
    return false
  }
}
