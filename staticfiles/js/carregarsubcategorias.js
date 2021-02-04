

$("#categoria").change(function() {

		// pego o valor do option selecionado
		var categoria = $('#categoria').find(":selected").val();

		// limpa as options do select cidades pelo id do select
		$("#subcategoria").empty();
		$('#subcategoria').append(`<option value="" disabled selected hidden>Carregando subcategorias..</option>`);

		// printa no console do navegador o estado selecionado
		// console.log(estado);

		// executo o ajax e passo a url e informação desejada
		$.ajax({

			 url: '/produtos/ajax/carregar-subcategoria/',
			 data: {
			   categoria: categoria
			 },

			 // caso o ajax ocorrer corretamente
			 success: function (data) {
                    $("#subcategoria").empty();
                    $('#subcategoria').append('<option value="" disabled selected hidden>Selecione a subcategoria</option>');

                    for(var i=0; i <  Object.keys(data['subcategorias']).length; i++ ){
                       	var subcategoria = data['subcategorias'][i];
                       	// console.log(subcategoria)

                        $('#subcategoria').append(`<option id="subcategoria" name="subcategoria" value='${subcategoria}'>${subcategoria}</option>`);
                    }
				// printa no console os dados retornados
			 	// console.log("buscou as cidades:");
				// console.log(data);

				// printa a quantidade de chaves do objeto 'cidades'
				// console.log(Object.keys(data['cidades']).length);


			  }
			});
})
