from seriados.models import Serie, Temporada, Episodio

Serie.objects.all()

nova = Serie(nome='Doctor Who')
nova.save()
print(nova.id)
print(nova.nome)

Serie.objects.all()