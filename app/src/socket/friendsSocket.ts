import { toast } from "react-toastify";
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
    }
    if (inviteFrom.type == 'accept'){
        toast.success(`${inviteFrom.target} прянял вашу заявку в друзья`)
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
