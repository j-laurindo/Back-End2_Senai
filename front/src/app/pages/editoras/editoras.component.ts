import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { EditorasService } from '../../services/editora.services';
import { Editora } from '../../models/editora';
import { AuthService } from '../../services/auth.services';

@Component({
  standalone: true,
  imports: [RouterLink],
  templateUrl: './editoras.component.html',
  styleUrls: ['./editoras.component.css'] 
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