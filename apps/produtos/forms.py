from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms
from django.forms import Textarea
import requests

from apps.produtos.models import Produto


def retorna_categorias():
    categorias = 'https://api.mercadolibre.com/sites/MLB/categories#json'
    requisicao_categorias = requests.get(categorias)
    lista = requisicao_categorias.json()

    dicionario = {}
    for indice, estados in enumerate(lista):
        dicionario[indice] = estados

    return dicionario

class CriarProdutoForm(forms.ModelForm):
    topico = forms.CharField(label='Tópico', required=True, help_text='Obrigatório', max_length=200)
    preco = forms.CharField(required=True, widget=forms.TextInput(
       attrs={'type': 'number','min': '0', 'step': "0.01"}))
    quantidade = forms.CharField(required=True, widget=forms.TextInput(
       attrs={'type': 'number','min': '0', 'onkeydown': "if(event.key==='.'){event.preventDefault();}"}))
    caracteristica = forms.CharField(
        label='Características do produto', help_text='Obrigatório', max_length=450, required=True, widget=forms.Textarea)

    class Meta:
        model = Produto
        fields = ('nome', 'preco', 'descricao', 'quantidade', 'imagem')

        widgets = {
            'descricao': Textarea(attrs={'cols': 60, 'rows': 10}),
            'caracteristica': Textarea(attrs={'cols': 60, 'rows': 10})
        }

    def __init__(self, *args, **kwargs):
        super(CriarProdutoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='form-group col-md-6'),
                Column('preco', css_class='form-group col-md-6'),
                Column('descricao', css_class='form-group col-md-6'),
                Column('quantidade', css_class='form-group col-md-6'),
                css_class='form-row'
            )
        )
        self.fields['nome'].widget.attrs['placeholder'] = 'Insira o nome do produto'
        self.fields['preco'].widget.attrs['placeholder'] = 'Insira o preço do produto'
        self.fields['descricao'].widget.attrs['placeholder'] = 'Insira a descrição do produto'
        self.fields['quantidade'].widget.attrs['placeholder'] = 'Insira a quantidade do produto'
        self.fields['caracteristica'].widget.attrs['placeholder'] = 'Insira as características do produto'
        self.fields['topico'].widget.attrs['placeholder'] = 'Insira o tópico do produto'


class EditarProduto(forms.ModelForm):
    topico = forms.CharField(label='Tópico', required=True, help_text='Obrigatório', max_length=200)
    preco = forms.CharField(required=True, widget=forms.TextInput(
       attrs={'type': 'number','min': '0', 'step': "0.01"}))
    quantidade = forms.CharField(required=True, widget=forms.TextInput(
       attrs={'type': 'number','min': '0', 'onkeydown': "if(event.key==='.'){event.preventDefault();}"}))
    caracteristica = forms.CharField(
        label='Características do produto', help_text='Obrigatório', max_length=450, required=True, widget=forms.Textarea)

    class Meta:
        model = Produto
        fields = ('nome', 'preco', 'descricao', 'quantidade')

        widgets = {
            'descricao': Textarea(attrs={'cols': 60, 'rows': 10}),
            'caracteristica': Textarea(attrs={'cols': 60, 'rows': 10})
        }

        def __init__(self, *args, **kwargs):
            super(EditarProduto, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                Row(
                    Column('nome', css_class='form-group col-md-6'),
                    Column('preco', css_class='form-group col-md-6'),
                    Column('descricao', css_class='form-group col-md-6'),
                    Column('quantidade', css_class='form-group col-md-6'),
                    css_class='form-row'
                )
            )
            self.fields['nome'].widget.attrs['placeholder'] = 'Insira o nome do produto'
            self.fields['preco'].widget.attrs['placeholder'] = 'Insira o preço do produto'
            self.fields['descricao'].widget.attrs['placeholder'] = 'Insira a descrição do produto'
            self.fields['quantidade'].widget.attrs['placeholder'] = 'Insira a quantidade do produto'
            self.fields['caracteristica'].widget.attrs['placeholder'] = 'Insira as características do produto'
            self.fields['topico'].widget.attrs['placeholder'] = 'Insira o tópico do produto'
