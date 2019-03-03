import { Component, OnInit, ViewChild, OnDestroy, Pipe, PipeTransform } from '@angular/core';
import { NavbarComponent } from '../navbar/navbar.component';
//import { APIService } from '../services/apiservice';
import { MatTableDataSource, MatPaginator, MatSort, MatIcon, MatSortable, MatSnackBar } from '@angular/material';
import { merge } from 'rxjs';
import { Observable } from 'rxjs/Rx';

import { Routes, RouterModule, Router, ActivatedRoute } from '@angular/router';
import 'rxjs/add/operator/filter';
import { switchMap } from 'rxjs/operators';

@Component({
  selector: 'app-jobs',
  templateUrl: './jobs.component.html',
  styleUrls: ['./jobs.component.css']
})
export class JobsComponent implements OnInit {

  constructor(
        //private apiService: APIService,
        private router: Router,
        private route: ActivatedRoute,
        public snackBar: MatSnackBar
    ) {  }

  location:any;
  address = "123 Street Lane";

/*    getLocationByID(id) {
        this.apiService.getLocationByID(id).subscribe((locData) => {
            this.location = locData;
        },
        error => {
            this.router.navigate(['./404']);
        });
    }*/

  ngOnInit() {
  }

}
