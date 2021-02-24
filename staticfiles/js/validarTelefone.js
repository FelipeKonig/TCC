// Verificar quando iniciar a pagina
$(document).ready(function () {
  if ($("[name='tipo_telefone']").find(":selected").val() == 'celular') {
    $('[name="numero_telefone"]').mask('(00) 00000-0000');
  }else{
    $('[name="numero_telefone"]').mask('(00) 0000-0000');
  }

  if ($("[name='tipo_telefone2']").find(":selected").val() == 'celular') {
    $("[name='numero_telefone2']").mask('(00) 00000-0000');
  }else{
    $("[name='numero_telefone2']").mask('(00) 0000-0000');
  }
});

// Verificar quando o usuario mudar
$(document).ready(function () {
  $("[name='tipo_telefone']").change(function() {
    let tipo_telefone = $("[name='tipo_telefone']").find(":selected").val();

    if (tipo_telefone == 'celular') {
      $('[name="numero_telefone"]').mask('(00) 00000-0000');
    }else{
      $('[name="numero_telefone"]').mask('(00) 0000-0000');
    }
  });
  $("[name='tipo_telefone2']").change(function() {
    let tipo_telefone = $("[name='tipo_telefone2']").find(":selected").val();

    if (tipo_telefone == 'celular') {
      $("[name='numero_telefone2']").mask('(00) 00000-0000');
    }else{
      $("[name='numero_telefone2']").mask('(00) 0000-0000');
    }
  });
});

// Verificar se o numero de telefone novo está correto
function validateForm() {

  var tipo_telefone = document.forms['editar']['tipo_telefone'].value;
  var numero_telefone = document.forms['editar']['numero_telefone'].value;

  if (tipo_telefone == 'celular') {
    if (numero_telefone.length < 15) {
      document.getElementsByName('numero_telefone')[0].style.borderColor = 'red';
      return false;
    }
  }else{
    if (numero_telefone.length < 14) {
      document.getElementsByName('numero_telefone')[0].style.borderColor = 'red';
      return false;
    }
  }

  var tipo_telefone2 = document.forms['editar']['tipo_telefone2'].value;
  var numero_telefone2 = document.forms['editar']['numero_telefone2'].value;

  if (tipo_telefone2 == 'celular') {
    if (numero_telefone2.length < 15 && numero_telefone2.length > 0) {
      document.getElementsByName('numero_telefone2')[0].style.borderColor = 'red';
      return false;
    }
  }else{
    if (numero_telefone2.length < 14 && numero_telefone2.length > 0) {
      document.getElementsByName('numero_telefone2')[0].style.borderColor = 'red';
      return false;
    }
  }

  return true;
}
