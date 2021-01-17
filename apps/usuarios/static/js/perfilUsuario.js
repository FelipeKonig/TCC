$(document).ready(function(){
  $('#id_cnpj').mask('00.000.000/0000-00');
  $( "#id_numeroTelefone" ).prop( "disabled", true );

   $('#id_telefone_selecionar').change(function(event){
   var telefone = event.currentTarget.value;
     if (telefone == 'fixo'){
     $('#id_numeroTelefone').mask('(00) 0000-0000');
     $( "#id_numeroTelefone" ).prop( "disabled", false );

     }
     else if(telefone == 'celular'){
        $('#id_numeroTelefone').mask('(00) 00000-0009');
         $( "#id_numeroTelefone" ).prop( "disabled", false );

     }
     else if(telefone == 'tipo'){
           $( "#id_numeroTelefone" ).prop( "disabled", true );
             $( "#id_numeroTelefone" ).val("")


     }
 });

});

