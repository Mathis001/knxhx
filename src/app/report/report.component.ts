import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.css']
})
export class ReportComponent implements OnInit {

  constructor() { }

    lat:any;
    lon:any;

    ngOnInit(){
        if(window.navigator.geolocation){
            navigator.geolocation.getCurrentPosition((position) => {
                this.lat = position.coords.latitude;
                this.lon = position.coords.longitude;
                console.log(position.coords.latitude);
                console.log(position.coords.longitude);
            });
        }
    }
}
