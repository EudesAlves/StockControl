from django.db import models
from django.utils.translation import gettext_lazy as _

class ClassificationTransfer(models.TextChoices):
    ENTRADA = 'Entrada', _('Entrada')
    TRANSFERENCIA = 'Transferência', _('Transferência')
    RETORNO_DEFEITO = 'Retorno Defeito', _('Retorno Defeito')
