import { Injectable, Inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { Autor } from "../models/autor";
import { environment } from "../environments/environment";

@Injectable({providedIn: 'root'})
export class AutoresService {
    private http = Inject(HttpClient) 
    private base = environment.apiBase

    listar(): Observable<Autor[]>{
        const url = `${this.base}autores`
        // linha 15 deu erro
        return this.http.get<Autor[]>(url)
    }
}