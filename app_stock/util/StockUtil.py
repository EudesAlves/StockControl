from enum import Enum

class ClassificationTransfer(Enum, str):
    ENTRADA = 'Entrada'
    TRANSFERENCIA = 'Transferência'
    RETORNO_DEFEITO = 'Retorno Defeito'
