$(document).ready(function () {

  var lista_produtos = document.getElementById("lista_pedidos");

  // .split() para separar as strings no Array
  lista_produtos = Array.from(lista_produtos.value.split(','));

  for(i=0; i < lista_produtos.length; i+=1){

    var produto_nome = lista_produtos[i];

    produto_nome = reparaString(produto_nome);

    var produto = document.getElementById(produto_nome);
    var valor = produto.value;
    var quant = valor.split('-');
    var quant_total = quant[1];

    for(j=1; j <= quant_total; j++){
      var item = produto_nome.split('-');
      if(j != quant[0]){
        $(`#select_quantidade_${item[1]}`).append(`<option value="${j}" >${j}</option>`);
      }else{
        $(`#select_quantidade_${item[1]}`).append(`<option value="${j}" selected >${j}</option>`);
      }
    }
  }

  function reparaString(produto_nome){
    var str = produto_nome.split(`'`);
    produto_nome = str[1];

    if(produto_nome.includes(`['`)){
      var str = produto_nome.split(`['`);
      produto_nome = str[1];
    }

    if(produto_nome.includes(`']`)){
      var str = produto_nome.split(`']`);
      produto_nome = str[1];
    }
    return produto_nome;
  }

  $("[name='select_quantidade']").change(function() {

    $.ajax({

  		url: '/pedidos/ajax/alterar-quantidade-produto-pedido/',
  		data: {
  		 produto: this.id,
       quantidade: this.value
  		 },
      success: function (data) {
        var produto = Object.values(data);
        document.getElementById(`preco_total_${produto[0].id}`).innerHTML = 'R$ ' + produto[0].precoTotal.toFixed(2);
        document.getElementById(`preco_total`).innerHTML = 'R$ ' + produto[1];
        document.getElementById(`quantidade_total`).innerHTML = produto[2];
      }
    });
  });

});
