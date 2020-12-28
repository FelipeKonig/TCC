from django.shortcuts import render
from django.views.generic import CreateView
from .forms import CustomUsuarioCreationForm, TelefoneForm
from .models import CustomUsuario
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
        context = {'formUser': formUser,
                   'formTelefone': formTelefone}
        return render(request, 'cadastros/usuario_cadastro.html', context)

    def post(self, request, *args, **kwargs):
        pass