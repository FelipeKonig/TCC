from django.contrib.auth import password_validation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms

from .validadoresForm import (
    validar_cpf,
    validar_data_nascimento,
)

from .models import (
    CustomUsuario, Endereco,
)

from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    PasswordChangeForm
)

CHOICES_EMPRESA_ADICIONAR = [('sim', 'Sim'),
                             ('nao', 'Não')]

CHOICES_TIPO_TELEFONE = [('tipo', 'Selecione'),
                        ('celular', 'Celular'),
                         ('fixo', 'Fixo')]


class DateInput(forms.DateInput):
    input_type = 'date'

    def clean(self, value):
        return super(DateInput, self).clean(value)


class CadastroPerfilUsuario(forms.ModelForm):
    data_nascimento = forms.DateField(widget=DateInput, label='Data de nascimento', help_text='Obrigatório',
                                      validators=[validar_data_nascimento])
    cpf = forms.CharField(label='CPF', help_text='Não obrigatório',
                          max_length=14, validators=[validar_cpf], required=False,
                          widget=forms.TextInput(attrs={'data-mask': "000.000.000-00"}))

    empresa_selecionar = forms.ChoiceField(label='Deseja adicionar a sua empresa?', choices=CHOICES_EMPRESA_ADICIONAR,
                                           widget=forms.RadioSelect)

    numeroTelefone = forms.CharField(label='Telefone', required=True, help_text='Origatório')

    telefone_selecionar = forms.ChoiceField(label='Selecione o tipo de telefone', choices=CHOICES_TIPO_TELEFONE,
                                            widget=forms.Select)
    foto = forms.ImageField(label='Foto do perfil')

<<<<<<< HEAD:usuarios/forms.py
class DateInput(forms.DateInput):
    input_type = 'date'
=======
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

                css_class='form-row'
            )
        )
>>>>>>> origin/ramonbecker:apps/usuarios/forms.py

        self.fields['first_name'].widget.attrs['placeholder'] = 'Insira seu primeiro nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Insira seu segundo nome'
        self.fields['cpf'].widget.attrs['placeholder'] = 'Insira seu cpf'


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


'''
class TelefoneForm(forms.ModelForm):
    # numeroFixo = forms.CharField(required=False, help_text='Não obrigatório', label='Telefone fixo', max_length=30)

    class Meta:
        model = Telefone
        fields = ('numero',)

    def __init__(self, *args, **kwargs):
        super(TelefoneForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs['placeholder'] = 'Insira o tipo do telefone'
        self.fields['numero'].widget.attrs['placeholder'] = 'Insira o número do telefone'
 '''


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


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ('estado', 'cidade', 'cep', 'rua', 'bairro', 'numero', 'complemento')
