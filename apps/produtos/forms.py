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

  #  subCategoria = forms.CharField(label='Subcategoria', required=False, max_length=250)
    #categoria = forms.ChoiceField(choices=(retorna_categorias()))

    class Meta:
        model = Produto
        fields = ('nome', 'preco', 'descricao', 'quantidade', 'imagem')

        widgets = {
            'descricao': Textarea(attrs={'cols': 60, 'rows': 10})
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
