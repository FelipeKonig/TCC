from datetime import date

from django.core.exceptions import ValidationError

from .models import (
    CustomUsuario,
    Telefone,
    Endereco
)

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)
from django import forms

CHOICES = [('sim', 'Sim'),
           ('nao', 'Não')]


def validar_data_nascimento(value):
    data_atual = date.today()
    data_atual_cortada = str(data_atual).split('-')
    data_digitada_cortada = str(value).split('-')

    ano_atual = int(data_atual_cortada[0])
    ano_atual_digitado = int(data_digitada_cortada[0])

    aux_calc_diferenca_ano = ano_atual - ano_atual_digitado

    if aux_calc_diferenca_ano < 18:
        raise ValidationError('A idade não pode ser menor que 18 anos')


class DateInput(forms.DateInput):
    input_type = 'date'

    def clean(self, value):
        return super(DateInput, self).clean(value)


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
    data_nascimento = forms.DateField(widget=DateInput, label='Data de nascimento', help_text='Obrigatório',
                                      required=True, validators=[validar_data_nascimento])

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.username = self.cleaned_data['email']
        user.data_nascimento = self.cleaned_data['data_nascimento']

        if commit:
            user.save()

        return user

    def __init__(self, *args, **kwargs):
        super(CustomUsuarioCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
                Column('data_nascimento', css_class='form-group col-md-6'),
                Column('password1', css_class='form-group col-md-6'),
                Column('password2', css_class='form-group col-md-6'),

                css_class='form-row'
            )
        )

        self.fields['first_name'].widget.attrs['placeholder'] = 'Insira seu primeiro nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Insira seu último nome'
        self.fields['email'].widget.attrs['placeholder'] = 'Insira seu e-mail'
        self.fields['password1'].widget.attrs['placeholder'] = 'Insira sua senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Insira sua senha novamente'


class TelefoneForm(forms.ModelForm):
    # numeroFixo = forms.CharField(required=False, help_text='Não obrigatório', label='Telefone fixo', max_length=30)

    class Meta:
        model = Telefone
        fields = ('numero',)

    def __init__(self, *args, **kwargs):
        super(TelefoneForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs['placeholder'] = 'Insira o tipo do telefone'
        self.fields['numero'].widget.attrs['placeholder'] = 'Insira o número do telefone'


class EnderecoForm(forms.ModelForm):

    class Meta:
        model = Endereco
        fields = ('estado', 'cidade','cep','rua', 'bairro', 'numero', 'complemento')

    # def __init__(self, *args, **kwargs):
    #     super(EnderecoForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.form_method = 'post'
    #     self.helper.attrs = {'novalidate': ''}
    #     self.fields['estado'].widget.attrs['placeholder'] = 'Insira o estado'
    #     self.fields['cidade'].widget.attrs['placeholder'] = 'Insira a cidade'
    #     self.fields['bairro'].widget.attrs['placeholder'] = 'Insira o bairro'
    #     self.fields['cep'].widget.attrs['placeholder'] = 'Insira o cep'
    #     self.fields['rua'].widget.attrs['placeholder'] = 'Insira a rua'
    #     self.fields['numero'].widget.attrs['placeholder'] = 'Insira o número'
    #     self.fields['complemento'].widget.attrs['placeholder'] = 'Insira o complemento'
