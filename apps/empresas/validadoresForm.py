from django.core.exceptions import ValidationError
from validate_docbr import CNPJ


def validar_cnpj(value):
    cnpj = CNPJ()
    if not cnpj.validate(value):
        raise ValidationError('CNPJ inválido')