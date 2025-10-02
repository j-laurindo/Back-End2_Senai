import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { LivrosService } from '../../services/livros.services';
import { Livro } from '../../models/livro';
import { AuthService } from '../../services/auth.services';

// Fazer o html dele
@Component({
  standalone: true,
  imports: [RouterLink],
  template:`
    <section style="max-width:900px;margin:2rem auto;padding:0 1rem">
      <h1>Livros</h1>

      @if (carregando()) {
        <p>Carregando…</p>
      } @else if (erro()) {
        <p style="color:#c62828">{{ erro() }}</p>
      } @else {
        <ul style="padding-left:1.25rem">
          @for (l of livro(); track l.id) {
            <li style="margin:.25rem 0">
              <strong>{{ l.titulo }} {{ l.subtitulo }}</strong>
              @if (l.autor) { • {{ l.autor }} }
              @if (l.editora) { <div style="color:#555">{{ l.editora }}</div> }
              @if (l.isbn) { <div style="color:#555">{{ l.isbn }}</div> }
              @if (l.descricao) { <div style="color:#555">{{ l.descricao }}</div> }
              @if (l.idioma) { <div style="color:#555">{{ l.idioma }}</div> }
              @if (l.ano_publicacao) { <div style="color:#555">{{ l.ano_publicacao }}</div> }
              @if (l.paginas) { <div style="color:#555">{{ l.paginas }}</div> }
              @if (l.preco) { <div style="color:#555">{{ l.preco }}</div> }
              @if (l.estoque) { <div style="color:#555">{{ l.estoque }}</div> }
              @if (l.desconto) { <div style="color:#555">{{ l.desconto }}</div> }
              @if (l.disponivel) { <div style="color:#555">{{l.disponivel }}</div> }
              @if (l.dimensoes) { <div style="color:#555">{{ l.dimensoes }}</div> }
              @if (l.peso) { <div style="color:#555">{{ l.peso }}</div> }
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
export class LivrosComponent {
  private svc = inject(LivrosService);
  private auth = inject(AuthService);   //Ver o token
  livro = signal<Livro[]>([]);
  carregando = signal(true);
  erro = signal<string | null>(null);

  constructor() {
    console.log("Token de acesso: ", this.auth.token());
    
    this.svc.listar().subscribe({
      next: (data) => { this.livro.set(data); this.carregando.set(false); },
      error: () => { this.erro.set('Falha ao carregar autores'); this.carregando.set(false); }
    });
  }
}