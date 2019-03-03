import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HomeComponent } from './home/home.component';
import { ReportComponent } from './report/report.component';
import { AdminComponent } from './admin/admin.component';
import { JobsComponent } from './jobs/jobs.component';


const routes: Routes = [
    {
        path: '',
        component: HomeComponent,
    },
    {
        path: 'report',
        component: ReportComponent,
    },
    {
        path: 'jobs',
        component: JobsComponent,
    },
    {
        path: 'jobs/:id',
        component: JobsComponent,
    },
    {
        path: 'admin',
        component: AdminComponent,
    },

];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule],
    providers: []
})
export class Routing { }
