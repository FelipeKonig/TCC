from .models import (
    CustomUsuario,
    Telefone,
    Endereco
)

from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    ReadOnlyPasswordHashField
)
from django import forms

CHOICES = [('sim', 'Sim'),
           ('nao', 'Não')]


class DateInput(forms.DateInput):
    input_type = 'date'


class CustomUsuarioCreationForm(UserCreationForm):
    radio_Endereco = forms.ChoiceField(label='Deseja adicionar mais um endereço?', choices=CHOICES, widget=forms.RadioSelect(),  help_text='Não obrigatório')
    data_nascimento = forms.DateField(widget=DateInput, label='Data de nascimento', help_text='Obrigatório', required=True)

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'email',  'telefone', 'cpf', 'endereco', 'foto')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.username = self.cleaned_data['email']

        if commit:
            user.save()

        return user

    def __init__(self, *args, **kwargs):
        super(CustomUsuarioCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Insira seu primeiro nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Insira seu último nome'
        self.fields['email'].widget.attrs['placeholder'] = 'Insira seu e-mail'
        self.fields['password1'].widget.attrs['placeholder'] = 'Insira sua senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Insira sua senha novamente'


class TelefoneForm(forms.ModelForm):
    numeroFixo = forms.CharField(required=False, help_text='Não obrigatório', label='Telefone fixo')

    class Meta:
        model = Telefone
        fields = ('numeroCelular',)

    def __init__(self, *args, **kwargs):
        super(TelefoneForm, self).__init__(*args, **kwargs)
        self.fields['numeroFixo'].widget.attrs['placeholder'] = 'Insira o seu telefone fixo'
        self.fields['numeroCelular'].widget.attrs['placeholder'] = 'Insira o seu telefone celular'


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ('rua', 'bairro', 'complemento', 'numero', 'cep')

    def __init__(self, *args, **kwargs):
        super(EnderecoForm, self).__init__(*args, **kwargs)
        self.fields['rua'].widget.attrs['placeholder'] = 'Insira a rua'
        self.fields['bairro'].widget.attrs['placeholder'] = 'Insira o bairro'
        self.fields['complemento'].widget.attrs['placeholder'] = 'Insira o complemento'
        self.fields['numero'].widget.attrs['placeholder'] = 'Insira o número'
        self.fields['cep'].widget.attrs['placeholder'] = 'Insira o cep'
