import { toast } from "react-toastify";
import { addFriendCurrent, addFriendIn, removeFriendOut } from "@/store/reducers/friendsSlice";
import store from "@/store/store";

export const chatSocket = new WebSocket(
    'wss://localhost:8000/ws/friend'
  );

export default function friendSockets(){
  let connected = false
  chatSocket.onopen = function(){
    console.log('Friends invite socket active')
    connected = true
  };

  chatSocket.onmessage = function(e) {
    const inviteFrom = JSON.parse(e.data)
    console.log(inviteFrom)
    if (inviteFrom.type == 'invite'){
      toast.warn(`Вам пришла заявка в друзья от ${inviteFrom.target}`)
      console.log('Диспатчу тут')
      store.dispatch(addFriendIn(inviteFrom.target))
    }
    if (inviteFrom.type == 'accept'){
      toast.success(`${inviteFrom.target} прянял вашу заявку в друзья`)
      store.dispatch(addFriendCurrent(inviteFrom.target))
      store.dispatch(removeFriendOut(inviteFrom.target))
    }
  }
  chatSocket.onerror = function(){
    console.log("Error")
  }
  chatSocket.onclose = function() {
    console.error('Friends socket not active');
  };
  return connected
}

type TNotificationType = 'accept' | 'invite'

export function sendNotificationFriend(type: TNotificationType, target: string){
  chatSocket.send(JSON.stringify({
    type: type,
    target: target
  }));
}
