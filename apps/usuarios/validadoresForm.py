from django.core.exceptions import ValidationError
from datetime import date
from validate_docbr import CPF


def validar_data_nascimento(value):
    data_atual = date.today()
    data_atual_cortada = str(data_atual).split('-')
    data_digitada_cortada = str(value).split('-')

    ano_atual = int(data_atual_cortada[0])
    ano_atual_digitado = int(data_digitada_cortada[0])

    aux_calc_diferenca_ano = ano_atual - ano_atual_digitado

    if aux_calc_diferenca_ano < 10:
        raise ValidationError('A idade não pode ser menor que 10 anos')


def validar_cpf(value):
    if value:
        cpf = CPF()
        if not cpf.validate(value):
            raise ValidationError('CPF inválido')
