from django.shortcuts import render
from django.views.generic import CreateView
from .forms import (
    CustomUsuarioCreationForm,
    TelefoneForm,
    EnderecoForm,
)
from .models import (
    CustomUsuario,
    Cidade,
    Estado,
)
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class SignUpView(SuccessMessageMixin, CreateView):
    #form_class = CustomUsuarioCreationForm
    #model = CustomUsuario
    success_url = reverse_lazy('home')
   # template_name = 'cadastros/usuario_cadastro.html'
    #success_message = 'Cadastro realizado com sucesso!'

    def get(self, request, *args, **kwargs):
        formUser = super().get_form(CustomUsuarioCreationForm)
        formTelefone = super().get_form(TelefoneForm)
        formEndereco = super().get_form(EnderecoForm)
        formEndereco1 = super().get_form(EnderecoForm)
        estados = Estado.objects.all()
        context = {'formUser': formUser,
                   'formTelefone': formTelefone,
                   'estados': estados,
                   'formEndereco': formEndereco,
                   'formEndereco1': formEndereco1
                   }
        return render(request, 'cadastros/usuario_cadastro.html', context)

    def post(self, request, *args, **kwargs):
        pass


#AJAX

def carregar_cidades(request):
    estado_id = request.GET.get('estado')
    cidades = Cidade.objects.filter(estado_id=estado_id).all()
    return render(request, 'cadastros/cidade_dropdown_list_options.html', {'cidades': cidades})