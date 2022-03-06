#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from seriados import models


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


s = models.Serie(nome="Falty Towers")
s.save()

t = models.Temporada(numero=1, series=s)
t.save()

import datetime
e = models.Episodio(data=datetime.date(1975,9,19), titulo ="A Tourch of Class", temporada =t)
e.save()

from django.contrib.auth import models as auth_models
u = auth_models.User.objects.get(pk=1)

r = models.Revisor(user=u)
r.save

re = models.ReviewEpisodio(episodio=e, revisor=r, nota='A')
re.save()

re.get_nota_display()   # Deve imprimir "Excelente"
re.nota                 # Deve imprimir 'A

 