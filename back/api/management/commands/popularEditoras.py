import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Editora

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--arquivo", default="population/Editoras.csv")
        parser.add_argument("--truncate", action="store_true")
        parser.add_argument("--update", action="store_true")

    @transaction.atomic
    def handle(self, *a, **o):
        # Dataframe que converterá os campos do arquivo csv e os passará para os campos do banco
        df = pd.read_csv(o["arquivo"], encoding="utf-8-sig")
        df.columns = [c.strip().lower().lstrip("\ufeff") for c in df.columns]

        if o['truncate']: Editora.objects.all().delete()

        df["editora"] = df["editora"].astype(str).str.strip()
        df["cnpj"] = df["cnpj"].astype(str).str.strip()
        df["endereco"] = df["endereco"].astype(str).str.strip()
        df["telefone"] = df["telefone"].astype(str).str.strip()
        df["email"] = df["email"].astype(str).str.strip()
        df["site"] = df["site"].astype(str).str.strip()

        if o["update"]:
            criados = atualizados = 0
            for r in df.itertuplas(index=False):
                _, created = Editora.objects.update_or_create(
                   editora = r.editora, cnpj = r.cnpj, endereco = r.endereco, 
                   telefone = r.telefone, email = r.email, site = r.site
                )

                criados += int(created)
                atualizados +=(not created)

            self.stdout.write(self.style.SUCCESS(f'Criados: {criados} | Atualizados: {atualizados}'))
        else:
            objs = [Editora(
                editora = r.editora, cnpj = r.cnpj, endereco = r.endereco, 
                   telefone = r.telefone, email = r.email, site = r.site
            ) for r in df.itertuples(index=False)]

            Editora.objects.bulk_create(objs, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f'Criados: {len(objs)}'))
            