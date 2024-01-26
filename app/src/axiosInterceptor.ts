import axios, { AxiosError, AxiosRequestConfig, AxiosHeaders } from 'axios';
import Cookies from 'js-cookie';

axios.interceptors.request.use(
  function (config: AxiosRequestConfig) {
    config.withCredentials = true;
    config.baseURL = import.meta.env.VITE_API_SERVER
    const newConfig = Object.assign({}, config, {
      headers: {
        ...(config.headers as AxiosHeaders),
        'X-CSRFTOKEN': Cookies.get('csrftoken'),
      },
    });
    return newConfig;
  },
  function (error: AxiosError) {
    return Promise.reject(error);
  },
);
