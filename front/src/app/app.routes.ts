import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { AutoresComponent } from './pages/authors/authors.component';

export const routes: Routes = [
    {path: '', component: HomeComponent},
    {path: 'home', component: HomeComponent},
    {path: 'autores', component: AutoresComponent}
];
