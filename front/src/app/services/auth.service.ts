import { Inject, Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable, tap } from "rxjs";
import { environment } from "../environments/environment";

type TokenPair = {access: string; refresh?: string}

const storage = {
    // Método para pegar o token no localStorage
    get: (k: string) => (typeof localStorage !== 'undefined' ? localStorage.getItem(k) : null),
    // Método para settar o token no localStorage
    set: (k: string, v: string) => { if (typeof localStorage !== 'undefined') localStorage.setItem(k, v)}
}

