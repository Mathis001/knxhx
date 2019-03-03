import { Component, OnInit, ViewChild, OnDestroy, Pipe, PipeTransform } from '@angular/core';
import { NavbarComponent } from '../navbar/navbar.component';
//import { APIService } from '../services/apiservice';
import { MatTableDataSource, MatPaginator, MatSort, MatIcon, MatSortable, MatSnackBar } from '@angular/material';
import { merge } from 'rxjs';
import { Observable } from 'rxjs/Rx';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
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
	) {	}

	id:any;
	location:any;
	address = "617 Cumberland Ave";
	city = "Knoxville"
	state = "TN"
	zip = "37902"
	lat = "35.9610544"
	lon = "-83.9206974"

	statusControl = new FormControl('', [Validators.required]);
	noteControl = new FormControl();

	url = "https://www.google.com/maps/place/"
		+ this.address.replace(/ /g,"+") + ",+" 
		+ this.city + ",+"
		+ this.state + "+"
		+ this.zip + "/@"
		+ this.lat + ","
		+ this.lon + ",18z"

	addressRedirect() {
		window.open(this.url, "_blank");
	}

	post() {
		if (this.statusControl.value) {
			this.statusControl.setValue('');
			this.router.navigate(['./jobs/' + parseInt(this.id + 1)]);
		}
	}

	getID() {
        this.route.params.subscribe( params => {
        	if (params.id) {
        		this.id = parseInt(params.id);
        	}else {
        		this.router.navigate(['./jobs/' + 1]);
        	}
        });
    }


/*	getLocationByID(id) {
		this.apiService.getLocationByID(id).subscribe((locData) => {
			this.location = locData;
		},
		error => {
			this.router.navigate(['./404']);
		});
	}*/

	ngOnInit() {
		this.getID();
	}

}
