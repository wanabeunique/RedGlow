import { toast } from "react-toastify";

export default function friendSockets(){
  let connected = false
  const chatSocket = new WebSocket(
    'wss://localhost:8000/ws/friend'
  );
  chatSocket.onopen = function(e){
    console.log('Friends invite socket active')
    connected = true
  };
  chatSocket.onmessage = function(e) {
    const inviteFrom = JSON.parse(e.data).invite.username
    toast.warn(`Вам пришла заявка в друзья от ${inviteFrom}`)
  };
  chatSocket.onerror = function(e){
    console.log("Error")
  }
  chatSocket.onclose = function(e) {
    console.error('Friends invite socket active');
  };
  return connected
}