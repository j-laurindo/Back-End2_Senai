import django_filters as df
from django.db.models import Q
from .models import Autor
 
class AutorFilters(df.FilterSet):
    nome = df.CharFilter(method="filter_nome")
    nacionalidade = df.CharFilter(method="nacionalidade", lookup_expr="iexact")
 
    def filter_nome(self, qs, name, value: str):
        if not value:
            return qs
        else:
            return qs.filter(Q(nome__icontains=value) | Q(sobrenome__icontains=value))
   
    def nacionalidade(self, qs, value: str):
        if not value:
            return qs
        return qs.filter(Q(nacionalidade_icontains=value))

    class Meta:
        model = Autor
        fields = []