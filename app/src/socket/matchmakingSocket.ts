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
      this.connected = true;
    };

    this.socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log(message);
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

  onMessage(callback) {
    this.callbacks.push(callback);
  }

  public startSearch(target_players: number, game: string) {
    console.log(
      JSON.stringify({
        type: 'enqueued',
        elo_filter: false,
        target_players,
        game,
      }),
    );
    return this.socket.send(
      JSON.stringify({
        type: 'enqueued',
        elo_filter: false,
        target_players,
        game,
      }),
    );
  }

  public close() {}
}

export default new MatchmakingSocketManager(
  `${import.meta.env.VITE_SOCKET_SERVER}/match_queue`,
);
