$(document).ready(function () {

  $(document).on('click','#button-minus', function(){
    let min = parseInt($('#quant_produto').attr('min'));
    let quant = parseInt($('#quant_produto').val());

    if(quant > min){
      quant -= 1;
      $('#quant_produto').val(quant);
    }
  });

  $(document).on('click','#button-plus', function(){
    let maximo = parseInt($('#quant_produto').attr('max'));
    let quant = parseInt($('#quant_produto').val());

    if(quant < maximo){
      quant += 1;
      $('#quant_produto').val(quant);
    }
  });

  $(document).on('click','.item-thumb', function(){
    var img = $(this).attr('src');
    $('#img_principal').attr('src', img);
  });
});
