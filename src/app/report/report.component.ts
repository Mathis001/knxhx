import { Component, OnInit, ViewChild, Input, HostListener } from '@angular/core';
import { MatTableDataSource, MatPaginator, MatSort } from '@angular/material';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { FormBuilder, FormGroup } from '@angular/forms';
import { merge } from 'rxjs';
import { Observable } from 'rxjs/Rx';
import { map, startWith} from 'rxjs/operators';
import { Routes, RouterModule, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';

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

    constructor(private _formBuilder: FormBuilder) {}

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

    ngOnInit() {
        this.gpsLocFormGroup = this._formBuilder.group({
            gpsLocCtrl: ['', Validators.required]
        });
        this.addressLocFormGroup = this._formBuilder.group({
            addressLocCtrl: ['', Validators.required]
        });
    }
}
