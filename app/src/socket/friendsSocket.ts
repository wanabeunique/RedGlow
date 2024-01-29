import { toast } from 'react-toastify';
import { acceptedInvite, addFriendCurrent, addFriendIn, incomingInvite, removeFriendOut } from '@/store/reducers/friendsSlice';
import store from '@/store/store';

class FriendSocketManager {
  private socket: WebSocket;
  private connected: boolean = false;

  constructor(socketUrl: string) {
    this.socket = new WebSocket(socketUrl);
    this.initSocket();
  }

  private initSocket() {
    this.socket.onopen = () => {
      console.log('Friends invite socket active');
      this.connected = true;
    };

    this.socket.onmessage = (event) => {
      const { type, username, photo } = JSON.parse(event.data);

      switch (type) {
        case 'accepted_invite':
          store.dispatch(acceptedInvite(username));
          toast.success(`${username} принял вашу заявку в друзья`);
          break;
        case 'incoming_invite':
          store.dispatch(incomingInvite(username));
          toast.warn(`Вам пришла заявка в друзья от ${username}`);
          break;
      }
    };

    this.socket.onerror = () => {
      console.log('Error');
    };

    this.socket.onclose = () => {
      console.error('Friends socket not active');
    };
  }

  public isConnected(): boolean {
    return this.connected;
  }

  public sendFriendEvent(type: IFriendSocketEvents, username: string) {
    console.log(this.socket.send(JSON.stringify({ type, username })))
    return this.socket.send(JSON.stringify({ type, username }));
  }

  public close() {
    this.socket.close();
  }
}

export type IFriendSocketEvents =
  | 'create_invite'
  | 'accept_invite'
  | 'cancel_invite'
  | 'decline_invite'
  | 'delete_friend';

export default new FriendSocketManager(`${import.meta.env.VITE_SOCKET_SERVER}/friend`)
