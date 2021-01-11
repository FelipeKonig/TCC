from datetime import date
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms

from .models import (
    CustomUsuario,
    Telefone
)

from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    PasswordChangeForm
)

CHOICES = [('sim', 'Sim'),
           ('nao', 'Não')]


class DateInput(forms.DateInput):
    input_type = 'date'

    def clean(self, value):
        return super(DateInput, self).clean(value)


def validar_data_nascimento(value):
    data_atual = date.today()
    data_atual_cortada = str(data_atual).split('-')
    data_digitada_cortada = str(value).split('-')

    ano_atual = int(data_atual_cortada[0])
    ano_atual_digitado = int(data_digitada_cortada[0])

    aux_calc_diferenca_ano = ano_atual - ano_atual_digitado

    if aux_calc_diferenca_ano < 15:
        raise ValidationError('A idade não pode ser menor que 18 anos')


def validar_cpf(value):

    valores_cpf_invalidos = {0: '00000000000', 1: '11111111111',
                             2: '22222222222', 3: '33333333333',
                             4: '44444444444', 5: '55555555555',
                             6: '66666666666', 7: '77777777777',
                             8: '88888888888', 9: '99999999999'
                             }

    cpf_cortado_digitos_finais = str(value).split('-')
    cpf_cortado_digitos_iniciais = cpf_cortado_digitos_finais[0].split('.')
    cpf_sem_formatacao = ''
    for numero in cpf_cortado_digitos_iniciais:
        cpf_sem_formatacao += numero

    cpf_sem_formatacao += cpf_cortado_digitos_finais[1]

    for key in valores_cpf_invalidos:
        if cpf_sem_formatacao == valores_cpf_invalidos[key]:
            raise ValidationError('CPF inválido')

    valores_cpf_finais = {0: int(cpf_cortado_digitos_finais[1][0]), 1: int(cpf_cortado_digitos_finais[1][1])}

    valores_cpf_iniciais = {0: int(cpf_cortado_digitos_iniciais[0][0]), 1: int(cpf_cortado_digitos_iniciais[0][1]),
                            2: int(cpf_cortado_digitos_iniciais[0][2]), 3: int(cpf_cortado_digitos_iniciais[1][0]),
                            4: int(cpf_cortado_digitos_iniciais[1][1]), 5: int(cpf_cortado_digitos_iniciais[1][2]),
                            6: int(cpf_cortado_digitos_iniciais[2][0]), 7: int(cpf_cortado_digitos_iniciais[2][1]),
                            8: int(cpf_cortado_digitos_iniciais[2][2]), 9: int(cpf_cortado_digitos_finais[1][0]),
                            10: int(cpf_cortado_digitos_finais[1][1])
                            }

    soma_valores_cpf_primeiro_digito = 0
    aux_peso = 10
    i = 0
    for key in valores_cpf_iniciais:
        soma_valores_cpf_primeiro_digito += valores_cpf_iniciais[key] * aux_peso
        aux_peso = aux_peso - 1
        i = i + 1
        if i == 9:
            break

    aux_multiplicao_peso_primeiro_digito = soma_valores_cpf_primeiro_digito * 10
    resto_divisao_segundo_digito = aux_multiplicao_peso_primeiro_digito % 11

    if resto_divisao_segundo_digito == valores_cpf_finais[0]:
        valores_cpf_iniciais[9] = valores_cpf_finais[0]

        aux_peso = 11
        soma_valores_cpf_segundo_digito = 0
        j = 0
        for key in valores_cpf_iniciais:
            soma_valores_cpf_segundo_digito += valores_cpf_iniciais[key] * aux_peso
            aux_peso = aux_peso - 1
            j = j + 1
            if j == 10:
                break

        aux_multiplicao_peso_segundo_digito = soma_valores_cpf_segundo_digito * 10
        resto_divisao_segundo_digito = aux_multiplicao_peso_segundo_digito % 11

        if resto_divisao_segundo_digito != valores_cpf_finais[1]:
            raise ValidationError('CPF inválido')

    else:
        raise ValidationError('CPF inválido')


class CadastroPerfilUsuario(forms.ModelForm):
    data_nascimento = forms.DateField(widget=DateInput, label='Data de nascimento', help_text='Obrigatório',
                                      validators=[validar_data_nascimento])
    cpf = forms.CharField(label='CPF', help_text='Obrigatório', max_length=14, validators=[validar_cpf])
    empresa_selecionar = forms.ChoiceField(label='Deseja adicionar a sua empresa?', choices=CHOICES,
                                           widget=forms.RadioSelect)
    numeroFixo = forms.CharField(required=False, help_text='Não obrigatório', label='Telefone fixo', max_length=30)
    numeroCelular = forms.CharField(required=True, help_text='Obrigatório', label='Telefone celular', max_length=30)
    foto = forms.ImageField(label='Foto do perfil')

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        super(CadastroPerfilUsuario, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
                Column('cpf', css_class='form-group col-md-6'),
                Column('data_nascimento', css_class='form-group col-md-6'),
                Column('numeroFixo', css_class='form-group col-md-6'),
                Column('numeroCelular', css_class='form-group col-md-6'),

                css_class='form-row'
            )
        )

        self.fields['first_name'].widget.attrs['placeholder'] = 'Insira seu primeiro nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Insira seu segundo nome'
        self.fields['cpf'].widget.attrs['placeholder'] = 'Insira seu cpf'
        self.fields['numeroFixo'].widget.attrs['placeholder'] = 'Insira seu telefone fixo'
        self.fields['numeroCelular'].widget.attrs['placeholder'] = 'Insira seu telefone celular'


class UsuarioLoginForm(AuthenticationForm):
    username = forms.EmailField(label='E-mail', help_text='Obrigatório')
    password = forms.CharField(widget=forms.PasswordInput(), label='Senha', help_text='Obrigatório')

    def __init__(self, *args, **kwargs):
        super(UsuarioLoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6'),
                Column('password', css_class='form-group col-md-6'),
                css_class='form-row'
            ))
        self.fields['username'].widget.attrs['placeholder'] = 'Insira seu e-mail'
        self.fields['password'].widget.attrs['placeholder'] = 'Insira sua senha'


class CustomUsuarioCreationForm(UserCreationForm):
    class Meta:
        model = CustomUsuario
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.username = self.cleaned_data['email']

        if commit:
            user.save()

        return user

    def __init__(self, *args, **kwargs):
        super(CustomUsuarioCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-6'),
                Column('password1', css_class='form-group col-md-6'),
                Column('password2', css_class='form-group col-md-6'),

                css_class='form-row'
            )
        )

        self.fields['email'].widget.attrs['placeholder'] = 'Insira seu e-mail'
        self.fields['password1'].widget.attrs['placeholder'] = 'Insira sua senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Insira sua senha novamente'


class EmailTokenSenhaForm(PasswordResetForm):
    email = forms.EmailField(required=True, help_text='Obrigatório', label='Email', max_length=254)

    def __init__(self, *args, **kwargs):
        super(EmailTokenSenhaForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Insira seu e-mail'


class ResetarSenhaForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha', 'class': 'password1'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        required=True

    )
    new_password2 = forms.CharField(
        label="Confirme sua senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Digite novamente sua senha', 'class': 'password2'}
        ),
        required=True,
        help_text='Obrigatório'
    )


class AlterarSenhaForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        required=True

    )
    new_password2 = forms.CharField(
        label="Confirme sua senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Digite novamente sua senha', 'class': 'password2'}
        ),
        required=True,
        help_text='Obrigatório'
    )

    def __init__(self, *args, **kwargs):
        super(AlterarSenhaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('password1', css_class='form-group col-md-6'),
                Column('password2', css_class='form-group col-md-6'),
                css_class='form-row'
            )
        )

        self.fields['old_password'].widget.attrs['placeholder'] = 'Insira sua senha antiga'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Insira sua nova senha'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Insira sua novamente sua nova senha'
