$(document).ready(function(){

  var value = $("#id_inscricaoEstadual").val();
  $("#id_inscricaoEstadual").prop('readonly', true);
  $("#id_inscricaoEstadual").prop('value', value);

  // Seleciona o select dos estados pelo id do select
  $("#estado").change(function() {

    // pego o valor do option selecionado
    var estado_selecionado = $('#estado').find(":selected").val();
    var estado = verifica_estado(estado_selecionado);

    $("#id_inscricaoEstadual").prop('readonly', false);
    $("#id_inscricaoEstadual").mask(estado.mascara);

  });

  function verifica_estado(sigla){
    let estados = [
      { uf: "AC", unidade_federativa: "Acre"               , mascara: "99.999.999/999-99" , quant_char: 13},
      { uf: "AL", unidade_federativa: "Alagoas"            , mascara: "99.9.99999-9"      , quant_char: 9},
      { uf: "AM", unidade_federativa: "Amazonas"           , mascara: "99.999.999-9"      , quant_char: 9},
      { uf: "AP", unidade_federativa: "Amapá"              , mascara: "99.999.999-9"      , quant_char: 9},
      { uf: "BA", unidade_federativa: "Bahia"              , mascara: "999999-99"         , quant_char: 8},
      { uf: "CE", unidade_federativa: "Ceará"              , mascara: "99.999.999-9"      , quant_char: 9},
      { uf: "DF", unidade_federativa: "Distrito Federal"   , mascara: "99.999999.999-99"  , quant_char: 13},
      { uf: "ES", unidade_federativa: "Espírito Santo"     , mascara: "99.999.999-9"      , quant_char: 9},
      { uf: "GO", unidade_federativa: "Goiás"              , mascara: "99.999.999-9"      , quant_char: 9},
      { uf: "MA", unidade_federativa: "Maranhão"           , mascara: "99.999.999-9"      , quant_char: 9},
      { uf: "MG", unidade_federativa: "Minas Gerais"       , mascara: "999.999.999/9999"  , quant_char: 13},
      { uf: "MS", unidade_federativa: "Mato Grosso do Sul" , mascara: "99.999.999-9"      , quant_char: 9},
      { uf: "MT", unidade_federativa: "Mato Grosso"        , mascara: "9999999999-9"      , quant_char: 11},
      { uf: "PA", unidade_federativa: "Pará"               , mascara: "99.999.999-9"      , quant_char: 9},
      { uf: "PB", unidade_federativa: "Paraíba"            , mascara: "99.999.999-9"      , quant_char: 9},
      { uf: "PE", unidade_federativa: "Pernambuco"         , mascara: "99.9.999.9999999-9", quant_char: 14},
      { uf: "PI", unidade_federativa: "Piauí"              , mascara: "99.999.999-9"      , quant_char: 9},
      { uf: "PR", unidade_federativa: "Paraná"             , mascara: "999.99999-99"      , quant_char: 10},
      { uf: "RJ", unidade_federativa: "Rio de Janeiro"     , mascara: "99.999.99-9"       , quant_char: 8},
      { uf: "RN", unidade_federativa: "Rio Grande do Norte", mascara: "99.999.999-9"      , quant_char: 9},
      { uf: "RO", unidade_federativa: "Rondônia"           , mascara: "99999999.99999-9"  , quant_char: 14},
      { uf: "RR", unidade_federativa: "Roraima"            , mascara: "99.999.999-9"      , quant_char: 9},
      { uf: "RS", unidade_federativa: "Rio Grande do Sul"  , mascara: "999/999999-9"      , quant_char: 10},
      { uf: "SC", unidade_federativa: "Santa Catarina"     , mascara: "999.999.999"       , quant_char: 9},
      { uf: "SE", unidade_federativa: "Sergipe"            , mascara: "9.99.999.999-9"    , quant_char: 10},
      { uf: "SP", unidade_federativa: "São Paulo"          , mascara: "99999999.9/999"    , quant_char: 12},
      { uf: "TO", unidade_federativa: "Tocantins"          , mascara: "99.99.999999-9"    , quant_char: 11},
    ];

    var estado = estados.find(objeto => objeto.uf === sigla);
    return estado;
  }

});
