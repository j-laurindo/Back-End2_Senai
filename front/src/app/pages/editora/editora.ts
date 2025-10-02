import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { EditorasService } from '../../services/editora.services';
import { Editora } from '../../models/editora';
import { AuthService } from '../../services/auth.services';

@Component({
  standalone: true,
  imports: [RouterLink],
  template:`
    <section style="max-width:900px;margin:2rem auto;padding:0 1rem">
      <h1>Editoras</h1>

      @if (carregando()) {
        <p>Carregando…</p>
      } @else if (erro()) {
        <p style="color:#c62828">{{ erro() }}</p>
      } @else {
        <ul style="padding-left:1.25rem">
          @for (e of editora(); track a.id) {
            <li style="margin:.25rem 0">
              <strong>{{ e.editora }}</strong>
              <strong>{{ e.cnpj }}</strong>
              @if (e.endereco) { • {{ e.endereco }} }
              @if (e.telefone) { <div style="color:#555">{{ e.telefone }}</div> }
              @if (e.email) { <div style="color:#555">{{ e.email }}</div> }
              @if (e.site) { <div style="color:#555">{{ e.site }}</div> }
            </li>
          }
        </ul>
      }

      <nav style="margin-top:1rem">
        <a routerLink="/">Voltar ao início</a>
      </nav>
    </section>
  `
})
export class EditorasComponent {
  private svc = inject(EditorasService);
  private auth = inject(AuthService);   //Ver o token
  editora = signal<Editora[]>([]);
  carregando = signal(true);
  erro = signal<string | null>(null);

  constructor() {
    console.log("Token de acesso: ", this.auth.token());
    
    this.svc.listar().subscribe({
      next: (data) => { this.editora.set(data); this.carregando.set(false); },
      error: () => { this.erro.set('Falha ao carregar autores'); this.carregando.set(false); }
    });
  }
}

