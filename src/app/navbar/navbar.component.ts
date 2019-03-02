import { Component, OnInit } from '@angular/core';
import { APIService } from '../services/apiservice';
import { LoadingBar } from '../services/loading-bar';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

    constructor(
        //private apiService: APIService,
        private loadingBar: LoadingBar,
    ) { }

    cookieObject:any;
    cookieData={};
    loginData={};
    salesAuth = false;
    supportAuth = false;
    adminAuth = false;
    isIn = false;   // store state

  
    toggleState() { // click handler
        let bool = this.isIn;
        this.isIn = bool === false ? true : false; 
    }

    ngOnInit() {
        //console.log();
    }

}
