import { Injectable } from '@angular/core';
import 'rxjs/add/operator/finally';

@Injectable()
export class LoadingBar {

    showSpinner = false;

    setSpinnerFlag(value: boolean) {
        Promise.resolve(null).then(() => this.showSpinner = value);
    }
    
}
