// formatando o input do cep
$(document).ready(function () {
    var $campo = $("#cep");
    $campo.mask('00000-000', {reverse: true});
});

// Seleciona o select dos estados pelo id do select
$("#estado").change(function() {

  // pego o valor do option selecionado
  var estado = $('#estado').find(":selected").val();

  // limpa as options do select cidades pelo id do select
  $("#cidade").empty();
  $('#cidade').append(`<option value="" disabled selected hidden>Carregando cidades..</option>`);

  // printa no console do navegador o estado selecionado
  // console.log(estado);

  // executo o ajax e passo a url e informação desejada
  $.ajax({
     url: '{% url "usuarios:ajax_carregar_cidades" %}',
     data: {
       'estado': estado
     },

     // caso o ajax ocorrer corretamente
     success: function (data) {

      // printa no console os dados retornados
      // console.log("buscou as cidades:");
      // console.log(data);

      // printa a quantidade de chaves do objeto 'cidades'
      // console.log(Object.keys(data['cidades']).length);

      $("#cidade").empty();

      $('#cidade').append('<option value="" disabled selected hidden>Selecione sua cidade</option>');

        for(var i=0; i < 	Object.keys(data['cidades']).length; i++ ){

          // pega o objeto que está na chave [i]
          var cidade = data['cidades'][i];
          // console.log(cidade);

          $('#cidade').append(`<option id="cidade" name="cidade" value='${cidade}'>${cidade} </option>`);

        }
      }
    });
});

$(document).ready(function(){
  $("#cep").keyup(function(){

    var cep = this.value;

    if(cep.length == 9){

        $.ajax({
           url: '{% url "usuarios:verificar_cep" %}',
           data: {
             'cep': cep
           },
             success: function (data) {

               // printa os dados retornados pelo ajax caso queira ver no console
               // console.log(data);

               try{
                 // retorna uma array dos pares de propriedade [chave, valor] com chave de string do próprio objeto
                 var endereco = Object.entries(data['cep'][0])

                 document.getElementById("cep").style.borderColor = 'lightGray';
                 $("#cep_msg").text('');

                 var rua = endereco[1];
                 document.getElementById("rua").value = rua[1];

                 var bairro = endereco[3];
                 document.getElementById("bairro").value = bairro[1];

                 var estado = $('#estado').find(":selected").val();

                 if(estado === ""){
                   var sigla_estado = endereco[5];
                   var estado = verifica_estado(sigla_estado[1]);
                   // console.log(estado);

                   var cidade = endereco[4];

                   $("#estado").empty();
                   $("#cidade").empty();

                   $('#estado').append(`<option id="estado" name="estado" value='${estado}|${sigla_estado[1]}'>${estado} </option>`);
                   $('#cidade').append(`<option id="cidade" name="cidade" value='${cidade[1]}'>${cidade[1]} </option>`);
                 }

               }catch{
                 document.getElementById("cep").style.borderColor = 'red';

                 $("#cep_msg").text('Cep inválido');
               }
             }
        });
    }
    function verifica_estado(sigla){
      let estados = [
        { uf: 'AL', unidade_federativa: 'Alagoas' },
        { uf: 'AC', unidade_federativa: 'Acre' },
        { uf: 'AP', unidade_federativa: 'Amapá' },
        { uf: 'AM', unidade_federativa: 'Amazonas' },
        { uf: 'BA', unidade_federativa: 'Bahia' },
        { uf: 'CE', unidade_federativa: 'Ceará' },
        { uf: 'DF', unidade_federativa: 'Distrito Federal' },
        { uf: 'ES', unidade_federativa: 'Espírito Santo' },
        { uf: 'GO', unidade_federativa: 'Goías' },
        { uf: 'MA', unidade_federativa: 'Maranhão' },
        { uf: 'MT', unidade_federativa: 'Mato Grosso' },
        { uf: 'MS', unidade_federativa: 'Mato Grosso do Sul' },
        { uf: 'MG', unidade_federativa: 'Minas Gerais' },
        { uf: 'PA', unidade_federativa: 'Pará' },
        { uf: 'PB', unidade_federativa: 'Paraíba' },
        { uf: 'PR', unidade_federativa: 'Paraná' },
        { uf: 'PE', unidade_federativa: 'Pernambuco' },
        { uf: 'PI', unidade_federativa: 'Piauí' },
        { uf: 'RJ', unidade_federativa: 'Rio de Janeiro' },
        { uf: 'RN', unidade_federativa: 'Rio Grande do Norte' },
        { uf: 'RS', unidade_federativa: 'Rio Grande do Sul' },
        { uf: 'RO', unidade_federativa: 'Rondônia' },
        { uf: 'RR', unidade_federativa: 'Roraíma' },
        { uf: 'SC', unidade_federativa: 'Santa Catarina' },
        { uf: 'SP', unidade_federativa: 'São Paulo' },
        { uf: 'SE', unidade_federativa: 'Sergipe' },
        { uf: 'TO', unidade_federativa: 'Tocantins' },
      ];

      var estado = estados.find(objeto => objeto.uf === sigla);
      // console.log(estado);
      // console.log(estado.unidade_federativa);
      return estado.unidade_federativa;
    }
  });
});

// validar os campos do formulário
(function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();
