from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms
from apps.empresas.models import Empresa
from .validadoresForm import validar_cnpj


class CadastroEmpresa(forms.ModelForm):

    inscricaoEstadual = forms.CharField(required=False, label='')
    inscricaoMunicipal = forms.CharField(required=False, widget=forms.TextInput(attrs={'maxlength': "15"}))

    class Meta:
        model = Empresa
        fields = ('razaoSocial', 'fantasia', 'logo', 'cnpj')

    def __init__(self, *args, **kwargs):
        super(CadastroEmpresa, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('razaoSocial', css_class='form-group col-md-6'),
                Column('fantasia', css_class='form-group col-md-6'),
                Column('cnpj', css_class='form-group col-md-6'),
                Column('inscricaoEstadual', css_class='form-group col-md-6'),
                Column('inscricaoMunicipal', css_class='form-group col-md-6'),
                css_class='form-row'
            )
        )
        self.fields['inscricaoMunicipal'].label = "Inscrição Municipal"
        self.fields['razaoSocial'].widget.attrs['placeholder'] = 'Insira a razão social'
        self.fields['fantasia'].widget.attrs['placeholder'] = 'Insira o nome fantasia'
        self.fields['cnpj'].widget.attrs['placeholder'] = 'Insira o CNPJ'
        self.fields['inscricaoEstadual'].widget.attrs['placeholder'] = 'Insira a inscrição estadual'
        self.fields['inscricaoMunicipal'].widget.attrs['placeholder'] = 'Insira a inscrição municipal'


class EditarEmpresaForm(forms.ModelForm):

    inscricaoEstadual = forms.CharField(required=False, label='')
    inscricaoMunicipal = forms.CharField(required=False, widget=forms.TextInput(attrs={'maxlength': "15"}))

    class Meta:
        model = Empresa
        fields = ('razaoSocial', 'fantasia', 'inscricaoEstadual', 'inscricaoMunicipal', 'cnpj')

    def __init__(self, *args, **kwargs):
        super(EditarEmpresaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('razaoSocial', css_class='form-group col-md-6'),
                Column('fantasia', css_class='form-group col-md-6'),
                Column('cnpj', css_class='form-group col-md-6'),
                Column('inscricaoEstadual', css_class='form-group col-md-6'),
                Column('inscricaoMunicipal', css_class='form-group col-md-6'),
                css_class='form-row'
            )
        )
        self.fields['inscricaoEstadual'].help_text = "Não Obrigatório"
        self.fields['inscricaoMunicipal'].label = "Inscrição Municipal"
        self.fields['inscricaoMunicipal'].help_text = "Não Obrigatório"
        self.fields['razaoSocial'].widget.attrs['placeholder'] = 'Insira a razão social'
        self.fields['fantasia'].widget.attrs['placeholder'] = 'Insira o nome fantasia'
        self.fields['cnpj'].widget.attrs['placeholder'] = 'Insira o CNPJ'
        self.fields['inscricaoEstadual'].widget.attrs['placeholder'] = 'Insira a inscrição estadual'
        self.fields['inscricaoMunicipal'].widget.attrs['placeholder'] = 'Insira a inscrição municipal'
