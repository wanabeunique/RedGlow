import { setData } from '@/store/reducers/gameAcceptingSlice';
import { startSearch, stopSearch } from '@/store/reducers/gameSlice';
import store from '@/store/store';

type matchmakingEvents = 'player_in_queue';

class MatchmakingSocketManager {
  private socket: WebSocket;
  private connected: boolean = false;
  private callbacks: [];

  constructor(socketUrl: string) {
    this.socket = new WebSocket(socketUrl);
    this.callbacks = [];
    this.initSocket();
  }

  private initSocket() {
    this.socket.onopen = () => {
      console.log('Matchmaking socket active');
      store.dispatch(stopSearch());
      this.connected = true;
    };

    this.socket.onmessage = (event) => {
      console.log(event);
      const message = JSON.parse(event.data);
      switch (message.type) {
        case 'player_in_queue':
          store.dispatch(startSearch());
          break;
        case 'match_found':
          store.dispatch(
            setData({
              isActive: true,
              timeToAccept: message['time_to_accept'],
            }),
          );
          store.dispatch(stopSearch())
          break;
        case 'match_canceled_by_time':
          store.dispatch(setData({ isActive: false }));
          break;
      }
      this.callbacks.forEach((callback) => callback(message));
    };

    this.socket.onerror = () => {
      console.log('Error');
    };

    this.socket.onclose = () => {};
  }

  public isConnected(): boolean {
    return this.connected;
  }

  onMessage(callback: Function) {
    this.callbacks.push(callback);
  }

  public startSearch(
    target_players: number,
    game: string,
    elo_filter: boolean,
  ) {
    let choosedGame = '';
    switch (game) {
      case 'civ5':
        choosedGame = `Sid Meier's Civilization V`;
        break;
      case 'civ6':
        choosedGame = `Sid Meier's Civilization VI`;
        break;
    }
    const data = JSON.stringify({
      type: 'enqueued',
      elo_filter,
      target_players: target_players,
      game: choosedGame,
    });
    console.log(data);
    return this.socket.send(data);
  }

  public close() {}
}

export default new MatchmakingSocketManager(
  `${import.meta.env.VITE_SOCKET_SERVER}/match_queue`,
);
