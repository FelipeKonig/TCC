from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms
from django.forms import Textarea

from apps.vitrines.models import Vitrine


class CadastroVitrine(forms.ModelForm):
    # descricao = forms.CharField(label='Descrição', widget=forms.Textarea(), help_text='Obrigatório', max_length=200)

    class Meta:
        model = Vitrine
        fields = ('nome', 'descricao')
        widgets = {
            'descricao': Textarea(attrs={'cols': 40, 'rows': 10})
        }

    def __init__(self, *args, **kwargs):
        super(CadastroVitrine, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='form-group col-md-6'),
                Column('descricao', css_class='form-group col-md-6'),
            )
        )
        self.fields['nome'].widget.attrs['placeholder'] = 'Insira o nome da vitrine'
        self.fields['descricao'].widget.attrs['placeholder'] = 'Insira a descrição da vitrine'


'''
class EditarVitrineForm(forms.ModelForm):
    #descricao = forms.CharField(label='Descrição', widget=forms.Textarea(), help_text='Obrigatório', max_length=200)

    class Meta:
        model = Vitrine
        fields = ('nome', 'descricao')
        widgets = {
            'descricao': Textarea(attrs={'cols': 50, 'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        super(EditarVitrineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='form-group col-md-6'),
            )
        )
        self.fields['nome'].widget.attrs['placeholder'] = 'Insira o nome da vitrine'

'''''
