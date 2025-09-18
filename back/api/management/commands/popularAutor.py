import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Autor

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--arquivo", default="population/autores.csv")
        parser.add_argument("--truncate", action="store_true")
        parser.add_argument("--update", action="store_true")

    @transaction.atomic
    def handle(self, *a, **o):
        # Dataframe que converterá os campos do arquivo csv e os passará para os campos do banco
        df = pd.read_csv(o["arquivo"], encoding="utf-8-sig")
        df.columns = [c.strip().lower().lstrip("\ufeff") for c in df.columns]

        if o['truncate']: Autor.objects.all().delete()

        df["nome"] = df["nome"].astype(str).str.strip()
        df["sobrenome"] = df["sobrenome"].astype(str).str.strip()
        df["data_nascimento"] = pd.to_datetime(df["data_nascimento"], errors="coerce", format="%Y-%m-%d").dt.date
        df["nacionalidade"] = df.get("nacionalidade", "").astype(str).str.strip().str.capitalize().replace({"": None})
        
        # Dataframe que consulta os nomes e sobrenomes vazios
        df = df.query("nome !='' and sobrenome != '' ")

        # Dataframe que deletará a linha na falta da data de nascimento
        df = df.dropna(subset=['data_nascimento'])

        if o["update"]:
            criados = atualizados = 0
            for r in df.itertuplas(index=False):
                _, created = Autor.objects.update_or_create(
                    nome = r.nome, sobrenome = r.sobrenome, data_nascimento = r.data_nascimento, 
                    defaults = {"nacionalidade": r.nacionalidade}
                )

                criados += int(created)
                atualizados +=(not created)

            self.stdout.write(self.style.SUCCESS(f'Criados: {criados} | Atualizados: {atualizados}'))
        else:
            objs = [Autor(
                nome = r.nome, sobrenome = r.sobrenome, data_nascimento = r.data_nascimento, nacionalidade = r.nacionalidade
            ) for r in df.itertuples(index=False)]

            Autor.objects.bulk_create(objs, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f'Criados: {len(objs)}'))
            