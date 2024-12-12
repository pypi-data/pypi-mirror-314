import { Injectable } from '@angular/core';
import {io} from "socket.io-client";

@Injectable({
  providedIn: 'root'
})
export class SocektioClientService {

  socket: any;
  constructor() { }
  setupSocketConnection(port:number) {
    this.socket = io('localhost:' + String(port));

    this.socket.on('connect', () => {
      console.log('Connected to socketio server');
    });
    this.socket.on('disconnect', () => {
      console.log('Disconnected from socketio server');
    });
  }
  disconnect() {
    if (this.socket) {
        this.socket.disconnect();
    }
  }
}
