import {Component, HostListener, OnDestroy, OnInit} from '@angular/core';
import {NgIf} from "@angular/common";
import {DEVELOP_MODE} from "../environments/environment";
import {SocektioClientService} from "./services/socektio-client.service";
import {EventCodes} from "./definitions/events";
import {SimpleAppConfig} from "./definitions/app_config";
import {FormsModule} from "@angular/forms";

declare var pywebview: any;
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [NgIf, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'ng-thor-frontend';
  socketio_ready = false;
  app_text = 'Starting app..'
  app_config: SimpleAppConfig = {username:'', token:''};
  @HostListener('window:pywebviewready', ['$event'])
  onPywebviewReady(event: any) {
    pywebview.api.get_socketio_port()
      .then((port: number) => {
        if(!DEVELOP_MODE){
          this.setup_socketio(port);
        }
      });
  }

  constructor(private socketioClientService: SocektioClientService) {}

  ngOnInit() {
      if(DEVELOP_MODE){
        this.setup_socketio(18495);
      }
  }

  setup_socketio(port: number){
      this.socketioClientService.setupSocketConnection(port);
      this.socketio_ready = true;
      this.app_text = 'SocketIO connected';

      this.socketioClientService.socket.on(EventCodes.REP_APP_PONG, (data: string) => {
        console.log('RX on socketioTestlogic:');
        console.log('\tEvent: ' + EventCodes.REP_APP_PONG);
        console.log('\tData: ' + data);
        this.app_text = 'PONG!!'
      });

      this.socketioClientService.socket.on(EventCodes.REP_APP_CONFIG, (data: string) => {
        console.log('RX on socketioTestlogic:');
        console.log('\tEvent: ' + EventCodes.REP_APP_CONFIG);
        console.log('\tData: ' + data);
        this.app_config = JSON.parse(data);
      });
  }

  ngOnDestroy() {
    this.socketioClientService.disconnect();
  }

  ping() {
    this.socketioClientService.socket.emit(EventCodes.REQ_APP_PING, null);
      this.app_text = 'ping...';
  }
  get_appconfig() {
    this.socketioClientService.socket.emit(EventCodes.REQ_APP_GET_CONFIG, null);
      this.app_config = {username:'', token:''};
  }
  set_appconfig() {
    this.socketioClientService.socket.emit(EventCodes.REQ_APP_SET_CONFIG, JSON.stringify(this.app_config));
      this.app_config = {username:'', token:''};
  }
}
