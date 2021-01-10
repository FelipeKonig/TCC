from datetime import date

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import (
    CustomUsuario,
    Telefone
)

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
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


class cadastroPerfilUsuario(forms.ModelForm):
    class Meta:
        model = CustomUsuario
        fields = ('')


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
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'email')

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
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
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
    numeroFixo = forms.CharField(required=False, help_text='Não obrigatório', label='Telefone fixo', max_length=30)

    class Meta:
        model = Telefone
        fields = ('numeroCelular',)

    def __init__(self, *args, **kwargs):
        super(TelefoneForm, self).__init__(*args, **kwargs)
        self.fields['numeroFixo'].widget.attrs['placeholder'] = 'Insira o seu telefone fixo'
        self.fields['numeroCelular'].widget.attrs['placeholder'] = 'Insira o seu telefone celular'


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
