from .models import CustomUsuario, Telefone
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django import forms


class CustomUsuarioCreationForm(UserCreationForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'email', 'data_nascimento', 'telefone', 'endereco', 'foto')

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
