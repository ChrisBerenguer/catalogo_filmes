from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from seriados import models


class Serie(models.Model):
    nome = models.CharField(max_length=70)

    def __str__(self) -> str:
        return self.nome


class Temporada(models.Model):
    numero = models.IntegerField()
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.serie.nome}: {self.numero}"


class Episodio(models.Model):
    data = models.DateField()
    titulo = models.CharField(max_length=200)
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('seriados:episodio_detalhes', kwargs={'pk': self.pk})

    def eh_antigo(self):
        import datetime
        if self.data < datetime.date(2000, 1, 1):
            return True
        return False


class Revisor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    reviews_episodios = models.ManyToManyField(
        Episodio, through='ReviewEpisodio')


class ReviewEpisodio(models.Model):
    NOTA_A = 'A'
    NOTA_B = 'B'
    NOTA_C = 'C'
    NOTAS_CHOICES = [
        (NOTA_A, _("Excelente")),
        (NOTA_B, _("Bom")),
        (NOTA_C, _("Ruim")),

    ]

    episodio = models.ForeignKey(Episodio, on_delete=models.CASCADE)
    revisor = models.ForeignKey(Revisor, on_delete=models.CASCADE)
    nota = models.CharField(
        max_length=1,
        choices=NOTAS_CHOICES,
        default=NOTA_B
    )
