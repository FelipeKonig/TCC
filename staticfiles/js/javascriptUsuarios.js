$(document).ready(function(){
			$("#id_numeroFixo").mask("(00) 0000-0000")
			$("#id_cep").mask("00.000-000")

			$("#id_numeroCelular").mask("(00) 0000-00009")

			$("#id_numeroCelular").blur(function(event){
				if ($(this).val().length == 15){
					$("#id_numeroCelular").mask("(00) 00000-0009")
				}else{
					$("#id_numeroCelular").mask("(00) 0000-00009")
				}
			})

		})
	         $('input[type="radio"]').click(function() {
                    var inputValue = $(this).attr("value");
                    var targetBox = $("." + inputValue);
                    $(".selectEndereco").not(targetBox).hide();
                    $(targetBox).show();
                });


		$("#estados").change(function () {
        var url = $("#estados").attr("data-cities-url");  // get the url of the `load_cities` view
        var estadoId = $(this).val();  // get the selected country ID from the HTML input

        $.ajax({                       // initialize an AJAX request
            url: url,                    // set the url of the request (= /persons/ajax/load-cities/ )
            data: {
                'estado': estadoId       // add the country id to the GET parameters
            },
            success: function (data) {   // `data` is the return of the `load_cities` view function
                $("#cidades").html(data);  // replace the contents of the city input with the data that came from the server

            }
        });

    });

    //Para o segundo endereço
    	$("#estados1").change(function () {
        var url = $("#estados1").attr("data-cities-url");  // get the url of the `load_cities` view
        var estadoId = $(this).val();  // get the selected country ID from the HTML input

        $.ajax({                       // initialize an AJAX request
            url: url,                    // set the url of the request (= /persons/ajax/load-cities/ )
            data: {
                'estado': estadoId       // add the country id to the GET parameters
            },
            success: function (data) {   // `data` is the return of the `load_cities` view function
                $("#cidades1").html(data);  // replace the contents of the city input with the data that came from the server

            }
        });

    });