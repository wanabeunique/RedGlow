import userService from '@/service/user.service';
import { Navigate } from 'react-router-dom';

export default function Steam() {
  let id = null;
  const searchParams = new URLSearchParams(location.search);
  const key = searchParams.get('openid.identity');
  const pattern = /https:\/\/steamcommunity.com\/openid\/id\/(\d+)/;

  if (key) {
    id = key.match(pattern);
  }

  if (id && id.length > 1) {
    userService.linkSteamAccount(id[1]);
  }

  return <Navigate to="/" />;
}
