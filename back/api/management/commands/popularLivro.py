import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Livro, Autor, Editora

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--arquivo_editoras", default="population/editoras.csv")
        parser.add_argument("--arquivo_autores", default="population/autores.csv")
        parser.add_argument("--arquivo_livros", default="population/livros.csv")
        parser.add_argument("--truncate", default="store_true")
        parser.add_argument("--update", default="store_true")
    
    @transaction.atomic
    def handle(self, *a, **o):
        df_autores = pd.read_csv(o["arquivo_autores"], encoding="utf-8-sig")
        df_editoras = pd.read_csv(o["arquivo_editoras"], encoding="utf-8-sig")
        df_livros = pd.read_csv(o["arquivo_livros"], encoding="utf-8-sig")

        df_autores.columns = [c.strip().lower().lstrip("\ufeff") for c in df_autores.columns]
        df_editoras.columns = [c.strip().lower().lstrip("\ufeff") for c in df_editoras.columns]
        df_livros.columns = [c.strip().lower().lstrip("\ufeff") for c in df_livros.columns]

        if o['truncate']: Livro.objects.all().delete()

        # Dataframes que coletam os dados do nome e ID dos autores
        df_autores["nome_completo"] = df_autores["nome"].str.strip() + " " + df_autores["sobrenome"].str.strip()

        # Mapa de autores - Exibição do nome e ID
        df_autores["id"] = df_autores.index + 1
        mapa_autores = dict(zip(df_autores["nome_completo"], df_autores["id"]))
        df_livros["id_autor"] = df_livros["autor"].map(mapa_autores)

        # Mapa de Editoras - Pegar ID; Criar mapa das editoras e definir o ID = nome da editora
        df_editoras["id"] = df_editoras.index + 1
        mapa_editoras = dict(zip(df_editoras["editora"], df_editoras["id"]))
        df_livros["id_editora"] = df_livros["editora"].map(mapa_editoras)

        # Criação da conversão do dataframe para .xlsx
        df_livros.to_excel("livros.xlsx", index=False)

        # Dataframes dos ID's de Editora e Livro
        df_livros["editora"] = df_livros["id_editora"]
        df_livros["autor"] = df_livros["id_autor"].astype(int)

        # Dataframes dos campos de Livros do csv
        df_livros["titulo"] = df_livros["titulo"].astype(str).str.strip()        
        df_livros["subtitulo"] = df_livros["subtitulo"].astype(str).str.strip()
        df_livros["descricao"] = df_livros["descricao"].astype(str).str.strip()
        df_livros["idioma"] = df_livros["idioma"].astype(str).str.strip()
        df_livros["ano_publicacao"] = df_livros["ano"].astype(int)
        df_livros["paginas"] = df_livros["paginas"].astype(int)
        df_livros["preco"] = df_livros["preco"].astype(float)
        df_livros["estoque"] = df_livros["estoque"].astype(int)
        df_livros["desconto"] = df_livros["desconto"].astype(float)
        df_livros["disponivel"] = df_livros["disponivel"].astype(bool)
        df_livros["dimensoes"] = df_livros["dimensoes"].astype(str).str.strip()
        df_livros["peso"] = df_livros["peso"].astype(float) 
        df_livros["isbn"] = df_livros["isbn"].astype(float)

        if o["update"]:
            criados = atualizados = 0
            for r in df_livros.itertuples(index=False):
                _, created = Livro.objects.update_or_create(
                   titulo = r.titulo, subtitulo = r.subtitulo, descricao = r.descricao, idioma = r.idioma,
                   ano_publicacao = r.ano_publicacao, paginas = r.paginas, preco = r.preco, estoque = r.estoque,
                   desconto = r.desconto, disponivel = r.disponivel, dimensoes = r.dimensoes, peso = r.peso,
                   autor_id = r.autor, editora_id = r.editora, isbn = r.isbn
                )

                criados += int(created)
                atualizados +=(not created)

            self.stdout.write(self.style.SUCCESS(f'Criados: {criados} | Atualizados: {atualizados}'))
        else:
            objs = [Livro(
                titulo = r.titulo, subtitulo = r.subtitulo, descricao = r.descricao, idioma = r.idioma,
                ano_publicacao = r.ano_publicacao, paginas = r.paginas, preco = r.preco, estoque = r.estoque,
                desconto = r.desconto, disponivel = r.disponivel, dimensoes = r.dimensoes, peso = r.peso,
                autor_id = r.autor, editora_id = r.editora, isbn = r.isbn
            ) for r in df_livros.itertuples(index=False)]

            Livro.objects.bulk_create(objs, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f'Criados: {len(objs)}'))
        