import { Injectable } from '@angular/core';
import { Observable } from "rxjs/Rx";
import { HttpClient } from "@angular/common/http";
import { environment } from '../../environments/environment';

@Injectable()
export class APIService {

    private apiUrl = environment.apiUrl;

    constructor(private httpClient: HttpClient) { }

    postGPS(data): Observable<any> {
        return this.httpClient.post(this.apiUrl+'location/post/gps', data, {})
    }

    postLocation(data): Observable<any> {
        return this.httpClient.post(this.apiUrl+'location/post/address', data, {})
    }
}

/*
    getAllSystems(): Observable<any> {
        return this.httpClient.get(this.apiUrl+'app/systems', {});
    }
    getAllConfigTypes(): Observable<any> {
        return this.httpClient.get(this.apiUrl+'app/system_config_types', {});
    }
    getRenewalConfigs(): Observable<any> {
        return this.httpClient.get(this.apiUrl+'app/renewal_config_types', {});
    }
    getAllClients(): Observable<any> {
        return this.httpClient.get(this.apiUrl+'app/clients_list', {});
    }


    getAllSystemIDs(): Observable<any> {
        return this.httpClient.get(this.apiUrl+'systems/system_ids', {});
    }


    postLicense(licenseData): Observable<any> {
        return this.httpClient.post(this.apiUrl+'system/post', licenseData, {})
    }
    getSystemInformationID(id): Observable<any> {
        return this.httpClient.get(this.apiUrl+'system/system_id/' + id, {});
    }
    getSystemInformationSerial(serial): Observable<any> {
        return this.httpClient.get(this.apiUrl+'system/serial/' + serial, {});
    }
    getSystemInformationLicense(license): Observable<any> {
        return this.httpClient.get(this.apiUrl+'system/license/' + license, {});
    }


    getRenewals(): Observable<any> {
        return this.httpClient.get(this.apiUrl+'renewals', {});
    }
    postRenewal(renewalData): Observable<any> {
        return this.httpClient.post(this.apiUrl+'renewal/post', renewalData, {})
    }
    getRenewalID(id): Observable<any> {
        return this.httpClient.get(this.apiUrl+'renewal/renewal_id/' + id, {});
    }
    getRenewalSystemID(id): Observable<any> {
        return this.httpClient.get(this.apiUrl+'renewal/system_id/' + id, {});
    }
    getRenewalSystemIDRenewalIndex(id, index): Observable<any> {
        return this.httpClient.get(this.apiUrl+'renewal/system_id/' + id + '/' + index, {});
    }
    getRenewalSerial(serial): Observable<any> {
        return this.httpClient.get(this.apiUrl+'renewal/serial/' + serial, {});
    }
    getRenewalLicense(license): Observable<any> {
        return this.httpClient.get(this.apiUrl+'renewal/license/' + license, {});
    }


    getAllOrderIDs(): Observable<any> {
        return this.httpClient.get(this.apiUrl+'order_ids', {});
    }


    getAllEmployees(): Observable<any> {
        return this.httpClient.get(this.apiUrl+'employees', {});
    }
    getEmployeeAuthLevels(): Observable<any> {
        return this.httpClient.get(this.apiUrl+'employees/tn_auths', {});
    }
    getEmployeesByAuth(auth): Observable<any> {
        return this.httpClient.get(this.apiUrl+'employees/tn_auth/' + auth, {});
    }
    getEmployeeName(name): Observable<any> {
        return this.httpClient.get(this.apiUrl+'employee/name/' + name, {});
    }
    getEmployeeLogin(login): Observable<any> {
        return this.httpClient.get(this.apiUrl+'employee/login/' + login, {});
    }

    */