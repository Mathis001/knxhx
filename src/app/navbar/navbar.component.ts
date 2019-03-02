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

    ngOnInit() {
        console.log();
    }

}
