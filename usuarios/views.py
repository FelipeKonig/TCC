from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from .forms import (
    CustomUsuarioCreationForm,
    TelefoneForm,
    EnderecoForm1
)
from .models import (
    CustomUsuario,
    Cidade,
    Estado,
    Telefone, Endereco
)
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class SignUpView(SuccessMessageMixin, CreateView):
    success_url = reverse_lazy('e-commerce:home')
    form_class = CustomUsuarioCreationForm
    template_name = 'cadastros/usuario_cadastro.html'

    '''
   def get(self, request, *args, **kwargs):
        formUser = super().get_form(CustomUsuarioCreationForm)
        formTelefone = super().get_form(TelefoneForm)
        formEndereco1 = super().get_form(EnderecoForm1)
        estados = Estado.objects.all()

        context = {'formUser': formUser,
                   'formTelefone': formTelefone,
                   'estados': estados,
                   'formEndereco1': formEndereco1
                   }
        return render(request, 'cadastros/usuario_cadastro.html', context)

    def post(self, request, *args, **kwargs):

        formUser = super().get_form(CustomUsuarioCreationForm)
        formTelefone = super().get_form(TelefoneForm)
        formEndereco1 = super().get_form(EnderecoForm1)
        
        if formUser.is_valid():
            first_name = formUser.cleaned_data['first_name']
            last_name = formUser.cleaned_data['last_name']
            email = formUser.cleaned_data['email']
            data_nascimento = formUser.cleaned_data['data_nascimento']
            password1 = formUser.cleaned_data['password1']
            password2 = formUser.cleaned_data['password2']

            if formTelefone.is_valid():
                telefoneFixo = formTelefone.cleaned_data['numeroFixo']
                telefoneCelular = formTelefone.cleaned_data['numeroCelular']
                aux_telefone, created = Telefone.objects.get_or_create(numeroFixo=telefoneFixo, numeroCelular=telefoneCelular)

            if formEndereco1.is_valid():
                rua = formEndereco1.cleaned_data['rua']
                bairro = formEndereco1.cleaned_data['bairro']
                numero = formEndereco1.cleaned_data['numero']
                complemento = formEndereco1.cleaned_data['complemento']
                cep = formEndereco1.cleaned_data['cep']

                id_Estado = request.POST.get('estados')
                id_Cidade = request.POST.get('cidades')
                estado = Estado.objects.get(id=id_Estado)
                cidade = Cidade.objects.get(id=id_Cidade)
                aux_endereco, created = Endereco.objects.get_or_create(rua=rua, bairro=bairro,
                                                                       numero=numero, complemento=complemento,
                                                                       cep=cep, cidade=cidade, estado=estado)

            aux_usuario, created = CustomUsuario.objects.get_or_create(first_name=first_name, last_name=last_name,
                                                                       email=email, data_nascimento=data_nascimento,
                                                                       password=password2, telefone=aux_telefone,
                                                                                                                                         endereco=aux_endereco)
            print('Usuário created', created)
            aux_usuario.save()

        estados = Estado.objects.all()
        context = {'formUser': formUser,
                   'formTelefone': formTelefone,
                   'estados': estados,
                   'formEndereco1': formEndereco1
                   }

        return render(request, 'cadastros/usuario_cadastro.html', context)
'''


# AJAX

def carregar_cidades(request):
    estado_id = request.GET.get('estado')
    cidades = Cidade.objects.filter(estado_id=estado_id).all()
    return render(request, 'cadastros/cidade_dropdown_list_options.html', {'cidades': cidades})
