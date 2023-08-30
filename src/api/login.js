import axios from "axios";

export default async function login(data){
  axios.post(
    'http://127.0.0.1:8000/user/session/',
    data,
    {withCredentials: true}
  )
  .then( (response) => {
    console.log(response)
    const headerKeys = Object.keys(response.headers);
    console.log(headerKeys);
    console.log('Set-Cookie:', response.headers['set-cookie'])
  })
}