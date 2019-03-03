import { Component, OnInit, ViewChild, Input, HostListener } from '@angular/core';
import { MatTableDataSource, MatPaginator, MatSort } from '@angular/material';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { FormBuilder, FormGroup } from '@angular/forms';
import { merge } from 'rxjs';
import { Observable } from 'rxjs/Rx';
import { map, startWith} from 'rxjs/operators';
import { Routes, RouterModule, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';
import { APIService } from '../services/apiservice';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.css']
})
export class ReportComponent implements OnInit {

    isLinear = true;
    isOptional = false;
    gpsLocFormGroup: FormGroup;
    addressLocFormGroup: FormGroup;
    data:any;

    constructor(
        private _formBuilder: FormBuilder,
        private apiService: APIService,
        private router: Router,
        public snackBar: MatSnackBar,
    ) {}

    getCoords() {
        if(window.navigator.geolocation){
            navigator.geolocation.getCurrentPosition((position) => {
                this.isOptional = !this.isOptional;
                this.gpsLocFormGroup.setValue({
                    gpsLocCtrl: (position.coords.latitude + ", " + position.coords.longitude), 
                });
                this.gpsLocFormGroup.markAsTouched();
            });
        }
    }

    submit() {
        this.data = {};
        if (this.gpsLocFormGroup.get('gpsLocCtrl').value) {
            this.data.latitude = this.gpsLocFormGroup.get('gpsLocCtrl').value.split(',', 1)[0];
            this.data.longitude = this.gpsLocFormGroup.get('gpsLocCtrl').value.split(' ', 2)[1];
            // console.log(this.data);
            this.apiService.postGPS(this.data).subscribe((returnData) => {
                this.snackBar.open('submitted!', '', {duration: 2000});
                this.router.navigate(['./home']);
            });
        } else if (this.addressLocFormGroup.get('addressLocCtrl').value) {
            this.data.address = this.addressLocFormGroup.get('addressLocCtrl').value;
            // console.log(this.data);
            this.apiService.postLocation(this.data).subscribe((returnData) => {
                this.snackBar.open('submitted!', '', {duration: 2000});
                this.router.navigate(['./home']);
            });
        }

    }

    ngOnInit() {
        this.gpsLocFormGroup = this._formBuilder.group({
            gpsLocCtrl: ['', Validators.required]
        });
        this.addressLocFormGroup = this._formBuilder.group({
            addressLocCtrl: ['', Validators.required]
        });
    }
}
